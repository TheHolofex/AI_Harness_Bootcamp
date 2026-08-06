<#
.SYNOPSIS
  Prepare or launch the deny-by-default P5 exposed OpenCode project.
.DESCRIPTION
  Resolves the pinned OpenCode config, force-disables every inherited MCP
  server, proves the exact edit allowlist, clears inherited inline config, and
  writes a sanitized boundary inventory. Any inconclusive check stops launch.
#>
param(
  [string]$StagingRoot = "$env:USERPROFILE\Documents\p5-staging",
  [string]$CourseRoot = "$env:USERPROFILE\Documents\HarnessBootcamp\AI_Harness_Bootcamp",
  [string]$Model = $env:HB_XAI_MODEL,
  [switch]$PrepareOnly
)

$ErrorActionPreference = "Stop"
$PinnedVersion = "1.18.11"
$CandidatePath = "out/triage_candidate.json"
$RequiredReads = @(
  "intake",
  "reference_corpus",
  "EXPECTED_INTAKE_FILES.json",
  "TRIAGE_CANDIDATE_SCHEMA.md"
)

if (-not (Test-Path -LiteralPath $StagingRoot -PathType Container)) {
  throw "Staging root missing: $StagingRoot"
}
foreach ($relative in $RequiredReads) {
  if (-not (Test-Path -LiteralPath (Join-Path $StagingRoot $relative))) {
    throw "Required staged input missing: $relative"
  }
}
if ([string]::IsNullOrWhiteSpace($Model)) {
  throw "HB_XAI_MODEL is empty. Set the course xAI model before launch."
}
if (-not (Get-Command npx -ErrorAction SilentlyContinue)) {
  throw "npx is unavailable; cannot run pinned OpenCode $PinnedVersion."
}
if ($args -contains "--auto" -or
    $env:OPENCODE_AUTO_APPROVE -eq "1" -or
    $env:OPENCODE_YOLO -eq "1") {
  throw "Auto-approval is forbidden for the exposed session."
}

$runtimeDir = Join-Path $StagingRoot "runtime"
New-Item -ItemType Directory -Path $runtimeDir -Force | Out-Null
$builder = Join-Path $CourseRoot "mission_flesh\p5\scripts\build_runtime_config.py"
if (-not (Test-Path -LiteralPath $builder -PathType Leaf)) {
  throw "Runtime config builder missing: $builder"
}

# Remove inline config supplied by the parent. A verified inline config is
# installed after MCP discovery.
Remove-Item "Env:OPENCODE_CONFIG_CONTENT" -ErrorAction SilentlyContinue

function Invoke-PinnedOpenCode {
  param([string[]]$OpenCodeArgs)
  $output = & npx -y "opencode-ai@$PinnedVersion" @OpenCodeArgs 2>&1
  if ($LASTEXITCODE -ne 0) {
    throw "Pinned OpenCode command failed: $($OpenCodeArgs -join ' ')`n$($output | Out-String)"
  }
  return $output
}

$reportedVersion = (Invoke-PinnedOpenCode -OpenCodeArgs @("--version") | Out-String).Trim()
if ($reportedVersion -ne $PinnedVersion) {
  throw "OpenCode version mismatch: expected $PinnedVersion, got $reportedVersion"
}

# First resolve inherited configuration so every inherited MCP server name can
# be overridden with enabled=false in the final, higher-priority config.
py -3 $builder --staging-root $StagingRoot --out-dir $runtimeDir
if ($LASTEXITCODE -ne 0) { throw "Initial runtime config build failed" }
$configPath = Join-Path $runtimeDir "opencode.json"
$env:OPENCODE_CONFIG = $configPath
$env:OPENCODE_CONFIG_DIR = $runtimeDir
$firstResolvedText = Invoke-PinnedOpenCode -OpenCodeArgs @("--pure", "debug", "config") | Out-String
try { $firstResolved = $firstResolvedText | ConvertFrom-Json } catch {
  throw "OpenCode debug config did not return JSON."
}
$mcpNames = @()
if ($null -ne $firstResolved.mcp) {
  $mcpNames = @($firstResolved.mcp.PSObject.Properties.Name | Sort-Object -Unique)
}

$buildArgs = @("-3", $builder, "--staging-root", $StagingRoot, "--out-dir", $runtimeDir)
foreach ($name in $mcpNames) { $buildArgs += @("--disable-mcp", $name) }
py @buildArgs
if ($LASTEXITCODE -ne 0) { throw "Final runtime config build failed" }

$configText = Get-Content -LiteralPath $configPath -Raw
$env:OPENCODE_CONFIG_CONTENT = $configText
$resolvedText = Invoke-PinnedOpenCode -OpenCodeArgs @("--pure", "debug", "config") | Out-String
try { $resolved = $resolvedText | ConvertFrom-Json } catch {
  throw "Final OpenCode debug config did not return JSON."
}

$edit = $resolved.permission.edit
$candidateRule = $null
if ($null -ne $edit) { $candidateRule = $edit.PSObject.Properties[$CandidatePath].Value }
if ($null -eq $edit -or $edit.'*' -ne "deny" -or $candidateRule -ne "allow") {
  throw "Resolved edit permission is not deny-all plus the exact candidate allowlist."
}
$extraEditAllows = @(
  $edit.PSObject.Properties |
    Where-Object { $_.Name -ne $CandidatePath -and $_.Value -eq "allow" }
)
if ($extraEditAllows.Count -gt 0) {
  throw "Resolved config contains an unexpected edit allow: $($extraEditAllows.Name -join ', ')"
}
$expectedReadAllows = @(
  "intake/**", "reference_corpus/**",
  "EXPECTED_INTAKE_FILES.json", "TRIAGE_CANDIDATE_SCHEMA.md"
)
$read = $resolved.permission.read
if ($null -eq $read -or $read.'*' -ne "deny") {
  throw "Resolved read permission does not deny all by default."
}
$actualReadAllows = @(
  $read.PSObject.Properties |
    Where-Object { $_.Value -eq "allow" } |
    ForEach-Object { $_.Name }
)
if (@(Compare-Object $expectedReadAllows $actualReadAllows).Count -gt 0) {
  throw "Resolved read allowlist contains a missing or unexpected path."
}
foreach ($denyName in @(
  "glob", "grep", "list", "bash", "task", "skill", "webfetch", "websearch",
  "external_directory", "doom_loop"
)) {
  if ($resolved.permission.PSObject.Properties[$denyName].Value -ne "deny") {
    throw "Resolved permission is not denied: $denyName"
  }
}
foreach ($property in $resolved.permission.PSObject.Properties) {
  if ($property.Value -eq "allow") {
    throw "Resolved config contains unexpected top-level allow: $($property.Name)"
  }
}

$resolvedMcp = @()
if ($null -ne $resolved.mcp) {
  foreach ($property in $resolved.mcp.PSObject.Properties) {
    $enabled = $property.Value.enabled
    if ($enabled -ne $false) {
      throw "MCP server remains enabled or ambiguous: $($property.Name)"
    }
    $resolvedMcp += [ordered]@{ name = $property.Name; enabled = $false }
  }
}

# This command must itself succeed. The JSON proof above is authoritative; the
# human-readable list is an additional live check, not a regex-based guess.
$null = Invoke-PinnedOpenCode -OpenCodeArgs @("--pure", "mcp", "list")
$agentText = Invoke-PinnedOpenCode -OpenCodeArgs @("--pure", "debug", "agent", "build") | Out-String
try { $resolvedAgent = $agentText | ConvertFrom-Json } catch {
  throw "OpenCode debug agent build did not return JSON."
}
$callableTools = @(
  $resolvedAgent.tools.PSObject.Properties |
    Where-Object { $_.Value -eq $true } |
    ForEach-Object { $_.Name } |
    Sort-Object -Unique
)
$allowedCallable = @("read", "edit", "write")
$unexpectedCallable = @($callableTools | Where-Object { $_ -notin $allowedCallable })
if ($unexpectedCallable.Count -gt 0) {
  throw "Resolved agent has a callable tool outside the allowlist: $($unexpectedCallable -join ', ')"
}

$hash = (Get-FileHash -LiteralPath $configPath -Algorithm SHA256).Hash.ToLowerInvariant()
$expectedHash = (Get-Content -LiteralPath (Join-Path $runtimeDir "runtime_config.sha256") -Raw).Trim()
if ($hash -ne $expectedHash) { throw "Runtime config hash mismatch after resolution." }

$inventory = [ordered]@{
  schema_version = 1
  source = "opencode --pure debug config, debug agent build, and mcp list"
  opencode_version = $reportedVersion
  project_root = (Resolve-Path -LiteralPath $StagingRoot).Path
  config_sha256 = $hash
  read_allowlist = @(
    "intake/**", "reference_corpus/**",
    "EXPECTED_INTAKE_FILES.json", "TRIAGE_CANDIDATE_SCHEMA.md"
  )
  write_allowlist = @($CandidatePath)
  permitted_builtin_permissions = @("read", "edit")
  callable_builtin_tools = @($callableTools)
  denied_permissions = @(
    "*", "glob", "grep", "list", "bash", "task", "skill", "webfetch", "websearch",
    "external_directory", "doom_loop"
  )
  mcp_servers = @($resolvedMcp)
  all_mcp_disabled = $true
  auto_approval = $false
}
$inventoryPath = Join-Path $runtimeDir "tool_inventory.json"
$inventory | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $inventoryPath -Encoding utf8

Write-Host "PASS P5 boundary: OpenCode $reportedVersion"
Write-Host "PASS project root: $StagingRoot"
Write-Host "PASS edit allowlist: $CandidatePath only"
Write-Host "PASS callable built-ins: $($callableTools -join ', ')"
Write-Host "PASS MCP: $($resolvedMcp.Count) inherited server(s), all disabled"
Write-Host "Runtime config SHA256: $hash"

if ($PrepareOnly) {
  Write-Host "PASS preparation only; no exposed session started."
  exit 0
}

$modelId = if ($Model.StartsWith("xai/")) { $Model } else { "xai/$Model" }
Set-Location -LiteralPath $StagingRoot
& npx -y "opencode-ai@$PinnedVersion" $StagingRoot --pure --model $modelId
exit $LASTEXITCODE
