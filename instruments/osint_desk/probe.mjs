// Live-feed probe. Run before class and before Stage 03.
//
// Both feeds are public, free and keyless. Neither needs an account. If one is
// down or has changed shape, this says so plainly rather than letting a learner
// spend twenty minutes debugging their own server against a broken source.

const OPENSKY = "https://opensky-network.org/api/states/all";
const AIS_LOCATIONS = "https://meri.digitraffic.fi/api/ais/v1/locations";
const AIS_VESSELS = "https://meri.digitraffic.fi/api/ais/v1/vessels";

// Digitraffic asks every client to identify itself and REQUIRES gzip. Without
// the encoding header it answers 406 and tells you why, which is better manners
// than most APIs manage.
const AIS_HEADERS = {
  "Accept": "application/json",
  "Accept-Encoding": "gzip",
  "Digitraffic-User": "AI-Harness-Bootcamp/osint-desk",
};

const results = [];
function record(name, ok, detail) {
  results.push({ name, ok, detail });
  process.stdout.write(`  ${ok ? "ok  " : "FAIL"} ${name}${detail ? ` — ${detail}` : ""}\n`);
}

async function probeOpenSky() {
  // A bounding box keeps the response small and is the polite way to ask.
  const url = `${OPENSKY}?lamin=51.0&lomin=-1.0&lamax=52.0&lomax=1.0`;
  const res = await fetch(url);
  const remaining = res.headers.get("x-rate-limit-remaining");
  if (!res.ok) return record("opensky reachable", false, `HTTP ${res.status}`);
  const body = await res.json();
  const states = body.states ?? [];
  record("opensky reachable", true, `HTTP 200, ${states.length} aircraft in the box`);
  record(
    "opensky state vector shape",
    states.length === 0 || states[0].length === 17,
    states.length ? `${states[0].length} fields per state` : "empty box, shape unchecked",
  );
  record(
    "opensky publishes a rate budget",
    remaining !== null,
    remaining !== null ? `x-rate-limit-remaining: ${remaining}` : "header absent",
  );
}

async function probeAis() {
  const loc = await fetch(AIS_LOCATIONS, { headers: AIS_HEADERS });
  if (!loc.ok) return record("digitraffic ais locations", false, `HTTP ${loc.status}`);
  const locBody = await loc.json();
  const feats = locBody.features ?? [];
  record("digitraffic ais locations", true, `HTTP 200, ${feats.length} vessels reporting`);

  const ves = await fetch(AIS_VESSELS, { headers: AIS_HEADERS });
  if (!ves.ok) return record("digitraffic ais vessels", false, `HTTP ${ves.status}`);
  const vesBody = await ves.json();
  record("digitraffic ais vessels", true, `HTTP 200, ${vesBody.length} vessel records`);

  // The gap that makes this a design problem rather than a passthrough: a
  // position knows only its MMSI. The name, destination and ship type live in
  // the other endpoint. Joining them is the server author's job.
  const locProps = new Set(Object.keys(feats[0]?.properties ?? {}));
  const vesProps = new Set(Object.keys(vesBody[0] ?? {}));
  const onlyMetadata = [...vesProps].filter((k) => !locProps.has(k));
  record(
    "positions carry no vessel name",
    !locProps.has("name") && vesProps.has("name"),
    `metadata-only fields: ${onlyMetadata.slice(0, 6).join(", ")}…`,
  );
  record("mmsi is the join key", locProps.has("mmsi") && vesProps.has("mmsi"));

  // Everything below is typed by whoever is aboard. Nothing verifies it.
  const named = vesBody.filter((v) => v.name && v.name.trim());
  record(
    "self-reported fields are present",
    named.length > 0,
    `${named.length} vessels broadcasting a name and destination they typed themselves`,
  );
}

async function main() {
  process.stdout.write("\nlive feeds\n");
  try { await probeOpenSky(); } catch (e) { record("opensky reachable", false, e.message); }
  try { await probeAis(); } catch (e) { record("digitraffic reachable", false, e.message); }

  const failed = results.filter((r) => !r.ok);
  process.stdout.write(
    failed.length
      ? `\nHOLD ${failed.length} of ${results.length} checks failed. Do not debug your own server against a feed that is down.\n`
      : `\nPASS both public feeds are up, keyless, and the shape is what the desk expects (${results.length} checks)\n`,
  );
  process.exitCode = failed.length ? 1 : 0;
}

main();
