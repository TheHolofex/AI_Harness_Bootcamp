<#
.SYNOPSIS
  Creates the P4 vault or launches a P4 OpenCode role with verified boundaries.
.DESCRIPTION
  Setup copies vault content without .opencode or .obsidian state. Director and
  Retriever clear inherited OpenCode overrides, verify the active Obsidian
  vault, inspect the resolved agent policy, and launch pinned OpenCode.
#>
[CmdletBinding()]
param(
  [Parameter(Position = 0)]
  [ValidateSet("Setup", "Director", "Retriever")]
  [string]$Mode = "Director",

  [string]$VaultRoot,
  [string]$ColdRoot,
  [string]$Model = $env:HB_XAI_MODEL
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$PinnedVersion = "1.18.11"
$CourseRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\..\..")).Path
$P4Root = Join-Path $CourseRoot "mission_flesh\p4"
$VaultSeed = Join-Path $P4Root "vault_seed"
$OpenCodeConfig = Join-Path $P4Root "controller\opencode.p4.json"
$OpenCodeAgents = Join-Path $VaultSeed ".opencode"

if ([string]::IsNullOrWhiteSpace($VaultRoot)) {
  $VaultRoot = Join-Path $env:USERPROFILE "Vaults\p4-vault"
}
if ([string]::IsNullOrWhiteSpace($ColdRoot)) {
  $ColdRoot = Join-Path ([Environment]::GetFolderPath("MyDocuments")) "p4-cold-query"
}

function Assert-File {
  param([string]$Path, [string]$Label)
  if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
    throw "$Label is missing: $Path"
  }
}

function Assert-Directory {
  param([string]$Path, [string]$Label)
  if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
    throw "$Label is missing: $Path"
  }
}

function Invoke-PinnedOpenCodeText {
  param(
    [string[]]$OpenCodeArgs,
    [switch]$Sensitive
  )

  $output = & npx -y "opencode-ai@$PinnedVersion" @OpenCodeArgs 2>&1
  if ($LASTEXITCODE -ne 0) {
    if ($Sensitive) {
      throw "Pinned OpenCode command failed. Sensitive resolved configuration was not printed."
    }
    throw "Pinned OpenCode command failed: $($OpenCodeArgs -join ' ')`n$($output | Out-String)"
  }
  return ($output | Out-String)
}

function Get-EffectivePermission {
  param(
    [object[]]$Rules,
    [string]$PermissionName,
    [string]$Resource = "*"
  )

  $effective = $null
  foreach ($rule in $Rules) {
    $permissionPattern = [string]$rule.permission
    $resourcePattern = [string]$rule.pattern
    if ([string]::IsNullOrWhiteSpace($resourcePattern)) {
      $resourcePattern = "*"
    }
    if (($PermissionName -like $permissionPattern) -and ($Resource -like $resourcePattern)) {
      $effective = [string]$rule.action
    }
  }
  return $effective
}

function Assert-Permission {
  param(
    [object[]]$Rules,
    [string]$PermissionName,
    [string]$Resource,
    [string]$Expected,
    [string]$AgentName
  )

  $actual = Get-EffectivePermission -Rules $Rules -PermissionName $PermissionName -Resource $Resource
  if ($actual -ne $Expected) {
    throw "$AgentName policy mismatch: $PermissionName on '$Resource' must be $Expected; resolved $actual."
  }
}

function Get-ResolvedAgent {
  param([string]$AgentName)

  $text = Invoke-PinnedOpenCodeText -OpenCodeArgs @(
    "--pure", "debug", "agent", $AgentName
  ) -Sensitive
  try {
    return ($text | ConvertFrom-Json)
  }
  catch {
    throw "OpenCode did not return valid JSON for agent '$AgentName'."
  }
}

function Assert-DirectorPolicy {
  $agent = Get-ResolvedAgent -AgentName "director"
  $rules = @($agent.permission)

  Assert-Permission $rules "external_directory" $VaultRoot "deny" "director"
  Assert-Permission $rules "edit" "operator/evidence/p4_run_contract.md" "allow" "director"
  Assert-Permission $rules "edit" "mission_flesh/p4/controller/opencode.p4.json" "deny" "director"
  Assert-Permission $rules "task" "worker_conus_rail_road" "allow" "director"
  Assert-Permission $rules "task" "general" "deny" "director"
  Assert-Permission $rules "obsidian_vault_read" "*" "allow" "director"
  Assert-Permission $rules "obsidian_vault_write" "*" "ask" "director"
  Assert-Permission $rules "obsidian_not_allowlisted" "*" "deny" "director"
  Assert-Permission $rules "websearch" "*" "deny" "director"
  Assert-Permission $rules "bash" "*" "deny" "director"

  foreach ($workerName in @(
    "worker_conus_rail_road",
    "worker_port_sealift_taiwan",
    "worker_constraints",
    "worker_protection"
  )) {
    $worker = Get-ResolvedAgent -AgentName $workerName
    $workerRules = @($worker.permission)
    Assert-Permission $workerRules "read" "operator/evidence/p4_run_contract.md" "allow" $workerName
    Assert-Permission $workerRules "read" "mission_flesh/p4/controller/opencode.p4.json" "deny" $workerName
    Assert-Permission $workerRules "edit" "operator/evidence/worker-output.json" "deny" $workerName
    Assert-Permission $workerRules "obsidian_vault_read" "*" "deny" $workerName
    Assert-Permission $workerRules "external_directory" $VaultRoot "deny" $workerName
    Assert-Permission $workerRules "websearch" "*" "deny" $workerName
    Assert-Permission $workerRules "bash" "*" "deny" $workerName
  }
}

function Assert-RetrieverPolicy {
  $agent = Get-ResolvedAgent -AgentName "retriever"
  $rules = @($agent.permission)

  Assert-Permission $rules "read" "anything.txt" "deny" "retriever"
  Assert-Permission $rules "edit" "anything.txt" "deny" "retriever"
  Assert-Permission $rules "external_directory" $VaultRoot "deny" "retriever"
  Assert-Permission $rules "obsidian_vault_read" "*" "allow" "retriever"
  Assert-Permission $rules "obsidian_vault_write" "*" "ask" "retriever"
  Assert-Permission $rules "obsidian_not_allowlisted" "*" "deny" "retriever"
  Assert-Permission $rules "websearch" "*" "deny" "retriever"
  Assert-Permission $rules "bash" "*" "deny" "retriever"
}

function Assert-ActiveP4Vault {
  Assert-Directory -Path $VaultRoot -Label "P4 vault"
  Assert-File -Path (Join-Path $VaultRoot "MOC.md") -Label "P4 vault root marker"
  Assert-Directory -Path (Join-Path $VaultRoot ".obsidian") -Label "Obsidian vault settings"
  if (Test-Path -LiteralPath (Join-Path $VaultRoot ".opencode")) {
    throw "The live vault contains .opencode policy. Archive it and run Setup again; do not launch OpenCode on the vault."
  }

  $headers = @{ Authorization = "Bearer $env:OBSIDIAN_REST_API_KEY" }
  try {
    $moc = Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:27123/vault/MOC.md" -Headers $headers
  }
  catch {
    throw "The authenticated P4 vault check failed. Keep Obsidian open on p4-vault and verify the HTTP server and API key."
  }
  $mocText = [string]$moc
  if (-not $mocText.Contains("# Map of contents") -or
      -not $mocText.Contains("[[Notes/Modes]]") -or
      -not $mocText.Contains("[[Notes/Route/Spine]]")) {
    throw "Port 27123 is serving the wrong Obsidian vault. Close other vault windows and reopen: $VaultRoot"
  }
}

function Initialize-P4Vault {
  Assert-Directory -Path $VaultSeed -Label "P4 vault seed"
  if (Test-Path -LiteralPath $VaultRoot) {
    throw "P4 vault already exists: $VaultRoot`nClose Obsidian and OpenCode, then archive that folder before running Setup again."
  }

  $vaultParent = Split-Path -Parent $VaultRoot
  New-Item -ItemType Directory -Path $vaultParent -Force | Out-Null
  New-Item -ItemType Directory -Path $VaultRoot | Out-Null

  foreach ($item in Get-ChildItem -LiteralPath $VaultSeed -Force) {
    if ($item.Name -in @(".opencode", ".obsidian")) {
      continue
    }
    Copy-Item -LiteralPath $item.FullName -Destination $VaultRoot -Recurse -Force
  }

  Remove-Item -LiteralPath (Join-Path $VaultRoot "Evidence\PERMISSIONS.example.json") -ErrorAction SilentlyContinue
  Remove-Item -LiteralPath (Join-Path $VaultRoot "Evidence\MCP_RECEIPTS.example.jsonl") -ErrorAction SilentlyContinue

  Assert-File -Path (Join-Path $VaultRoot "MOC.md") -Label "P4 vault root marker"
  if (Test-Path -LiteralPath (Join-Path $VaultRoot ".opencode")) {
    throw "Setup copied .opencode into the live vault. Stop and report this course-pack error."
  }

  $probe = Join-Path $VaultRoot "p4-write-probe-$([Guid]::NewGuid().ToString('N')).tmp"
  try {
    Set-Content -LiteralPath $probe -Value "p4 writable" -NoNewline
    Remove-Item -LiteralPath $probe -Force
  }
  catch {
    throw "The vault is not writable as the current Windows user: $VaultRoot`nDo not change ACLs or run as administrator. Choose a normal local user folder.`n$($_.Exception.Message)"
  }

  Write-Host "PASS P4 setup"
  Write-Host "Obsidian vault: $VaultRoot"
  Write-Host "OpenCode project: $CourseRoot"
  Write-Host "The live vault is writable and contains no .opencode or .obsidian state."
  Write-Host "Next: Obsidian > Manage vaults > Open folder as vault, then select the p4-vault folder itself."
}

Assert-Directory -Path $P4Root -Label "P4 course module"

if ($Mode -eq "Setup") {
  Initialize-P4Vault
  return
}

Assert-File -Path $OpenCodeConfig -Label "P4 OpenCode config"
Assert-Directory -Path $OpenCodeAgents -Label "P4 OpenCode agent directory"

if ([string]::IsNullOrWhiteSpace($Model)) {
  throw "HB_XAI_MODEL is empty. Set the course xAI model before launch."
}
if ([string]::IsNullOrWhiteSpace($env:OBSIDIAN_REST_API_KEY)) {
  throw "OBSIDIAN_REST_API_KEY is empty. Copy the standalone API key from Obsidian first."
}
if ($env:OBSIDIAN_REST_API_KEY -eq "PASTE_YOUR_STANDALONE_OBSIDIAN_API_KEY_HERE") {
  throw "Replace the Obsidian API-key placeholder before launch."
}
if ($env:OBSIDIAN_REST_API_KEY -match '^Bearer\s') {
  throw "Use the standalone Obsidian API key without the Bearer prefix."
}
if (-not (Get-Command npx -ErrorAction SilentlyContinue)) {
  throw "npx is unavailable. Complete the Node.js pre-work before P4."
}
if ($env:OPENCODE_YOLO -in @("1", "true", "TRUE") -or
    $env:OPENCODE_AUTO_APPROVE -in @("1", "true", "TRUE")) {
  throw "Automatic approval is enabled. Disable it so MCP writes remain ask-gated."
}

# Inline permission/config values have higher precedence than the course files.
# Remove inherited values so an earlier exercise cannot change this run.
Remove-Item "Env:OPENCODE_CONFIG_CONTENT" -ErrorAction SilentlyContinue
Remove-Item "Env:OPENCODE_PERMISSION" -ErrorAction SilentlyContinue
$env:OPENCODE_CONFIG = $OpenCodeConfig
$env:OPENCODE_CONFIG_DIR = $OpenCodeAgents

Assert-ActiveP4Vault

if ($Mode -eq "Director") {
  New-Item -ItemType Directory -Path (Join-Path $CourseRoot "operator\evidence") -Force | Out-Null
  $projectRoot = $CourseRoot
  $agentName = "director"
}
else {
  if (-not (Test-Path -LiteralPath $ColdRoot)) {
    New-Item -ItemType Directory -Path $ColdRoot -Force | Out-Null
  }
  Assert-Directory -Path $ColdRoot -Label "Cold retrieval project"
  $coldItems = @(Get-ChildItem -LiteralPath $ColdRoot -Force)
  if ($coldItems.Count -ne 0) {
    throw "Cold retrieval project is not empty: $ColdRoot`nArchive it, then run Retriever again."
  }
  $projectRoot = $ColdRoot
  $agentName = "retriever"
}

# Resolve and validate the same project root that the interactive session uses.
Set-Location -LiteralPath $projectRoot

$version = (Invoke-PinnedOpenCodeText -OpenCodeArgs @("--version")).Trim()
if ($version -ne $PinnedVersion) {
  throw "OpenCode version mismatch: expected $PinnedVersion, got $version."
}

$configText = Invoke-PinnedOpenCodeText -OpenCodeArgs @("--pure", "debug", "config") -Sensitive
try {
  $resolved = $configText | ConvertFrom-Json
}
catch {
  throw "OpenCode did not return valid resolved configuration JSON."
}
$obsidianProperty = $resolved.mcp.PSObject.Properties["obsidian"]
if ($null -eq $obsidianProperty) {
  throw "Resolved OpenCode configuration does not contain the Obsidian MCP server."
}
$obsidian = $obsidianProperty.Value
if ($obsidian.enabled -ne $true -or $obsidian.url -ne "http://127.0.0.1:27123/mcp/") {
  throw "Resolved Obsidian MCP endpoint is not the P4 HTTP endpoint."
}
$expectedAuthorization = "Bearer $env:OBSIDIAN_REST_API_KEY"
if ($obsidian.headers.Authorization -ne $expectedAuthorization) {
  throw "Resolved Obsidian authorization header does not match the current API key."
}

if ($Mode -eq "Director") {
  Assert-DirectorPolicy
}
else {
  Assert-RetrieverPolicy
}

$mcpStatus = Invoke-PinnedOpenCodeText -OpenCodeArgs @("--pure", "mcp", "list")
if ($mcpStatus -notmatch "obsidian") {
  throw "OpenCode did not report the Obsidian MCP server."
}

$modelId = $Model
if (-not $modelId.StartsWith("xai/")) {
  $modelId = "xai/$modelId"
}

Write-Host "PASS P4 launch boundary"
Write-Host "OpenCode $version"
Write-Host "Agent: $agentName"
Write-Host "OpenCode project: $projectRoot"
Write-Host "Obsidian vault: $VaultRoot (MCP only; Windows permissions unchanged)"
Write-Host $mcpStatus.Trim()

& npx -y "opencode-ai@$PinnedVersion" $projectRoot --pure --agent $agentName -m $modelId
if ($LASTEXITCODE -ne 0) {
  throw "OpenCode exited with code $LASTEXITCODE."
}
