# The open source desk — kit

Material for building an MCP server over live public feeds.

## The two feeds

Both are free, keyless, and need no account. Neither is a scrape: both are
published for this purpose.

| Feed | What it gives | Notes |
|---|---|---|
| **Digitraffic Marine AIS** — `meri.digitraffic.fi/api/ais/v1/` | `locations` returns live vessel positions as GeoJSON; `vessels` returns the metadata each vessel broadcasts about itself | Fintraffic open data, **CC BY 4.0**. Requires a `Digitraffic-User` header and **gzip** — without `Accept-Encoding: gzip` it answers `406` and tells you so |
| **OpenSky Network** — `opensky-network.org/api/states/all` | Live aircraft state vectors, 17 fields each | Anonymous access works. Publishes your remaining budget in an `x-rate-limit-remaining` header. Use a bounding box |

**The two AIS endpoints do not join themselves.** A position carries an `mmsi`
and nothing else identifying; the name, destination, call sign and ship type
live in the other endpoint. Joining them is the server author's work, and it is
the difference between a passthrough and a surface worth connecting to.

**Almost everything a vessel says about itself is unverified.** Name,
destination, call sign, ship type and draught are typed by whoever is aboard.
Position, speed, course and navigational status come off the transponder. A
server that returns both without saying which is which has destroyed the only
thing that lets a reader weigh them.

## What is here

| Path | What it is |
|---|---|
| `probe.mjs` | Checks both feeds are up, keyless, and still the shape the desk expects. Run before class and before Stage 03 |
| `specimen/server.mjs` | A server to read in Stage 01. **Inert** — every handler refuses, it reaches no network and opens no file. Its payload is its tool descriptions |
| `starter/server.mjs` | Skeleton with one tool written end to end: the join, a row ceiling, decoded status codes, and observed facts separated from self-reported ones |
| `fixtures/ais_vessels_planted.json` | Captured vessel metadata with three planted records. Two carry text aimed at whoever reads them next; one is planted and completely ordinary |
| `smoke.mjs` | Offline checks over all three. No network, so a public feed having a bad afternoon never turns the build red |

## The specimen

`specimen/server.mjs` is modelled on patterns found in real community servers.
It does nothing. Running it returns a refusal from every tool, because a course
does not ship a working attack — the lesson is in reading it, not in surviving
it.

Its four findings are in the file as `FINDINGS`, and
`node specimen/server.mjs --findings` prints them. Read the descriptions
yourself before you look.

## Running it

```
npm ci --ignore-scripts --no-audit --no-fund
npm run probe     # live: are both feeds up?
npm run smoke     # offline: is the kit intact?
node specimen/server.mjs --findings
```

Attribution, if you publish anything built on the marine feed: *Finnish
Transport Infrastructure Agency / Fintraffic, Digitraffic, CC BY 4.0.*
