// Starter skeleton for the open source desk.
//
// One tool is written for you, end to end, because the craft is easier to copy
// than to describe. Everything it does is something Stages 04 to 06 will ask
// you to justify: the description answers four questions, the result is capped,
// the coded fields are decoded, and every field a stranger controls is labelled
// as one.
//
// Add your own tools below the marker. Two to five in total. Read-only.

import { McpServer } from "@modelcontextprotocol/server";
import { serveStdio } from "@modelcontextprotocol/server/stdio";
import * as z from "zod/v4";

const AIS_LOCATIONS = "https://meri.digitraffic.fi/api/ais/v1/locations";
const AIS_VESSELS = "https://meri.digitraffic.fi/api/ais/v1/vessels";
const AIS_HEADERS = {
  "Accept": "application/json",
  "Accept-Encoding": "gzip", // Digitraffic answers 406 without this
  "Digitraffic-User": "AI-Harness-Bootcamp/osint-desk",
};

// A ceiling you cannot exceed by accident. The feed returns over a thousand
// vessels; a thousand rows in somebody's context is damage you cannot undo.
const MAX_ROWS = 20;

// AIS navigational status is an integer on the wire. `navStat: 0` tells a model
// nothing, so it never leaves this server as a number.
const NAV_STATUS = {
  0: "under way using engine", 1: "at anchor", 2: "not under command",
  3: "restricted manoeuvrability", 4: "constrained by draught", 5: "moored",
  6: "aground", 7: "engaged in fishing", 8: "under way sailing",
  15: "undefined",
};

const SHIP_TYPE = {
  30: "fishing", 31: "towing", 35: "military", 36: "sailing", 37: "pleasure craft",
  50: "pilot vessel", 51: "search and rescue", 52: "tug", 53: "port tender",
  60: "passenger", 70: "cargo", 80: "tanker", 90: "other",
};
const shipType = (n) => SHIP_TYPE[n] ?? (n >= 60 && n < 70 ? "passenger" : n >= 70 && n < 80 ? "cargo" : n >= 80 && n < 90 ? "tanker" : `unmapped code ${n}`);

// Great-circle distance, kilometres.
function km(lat1, lon1, lat2, lon2) {
  const R = 6371, r = Math.PI / 180;
  const a = Math.sin(((lat2 - lat1) * r) / 2) ** 2 +
    Math.cos(lat1 * r) * Math.cos(lat2 * r) * Math.sin(((lon2 - lon1) * r) / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

async function getJson(url) {
  const res = await fetch(url, { headers: AIS_HEADERS });
  if (!res.ok) throw new Error(`${url} answered HTTP ${res.status}`);
  return res.json();
}

export function createDeskServer() {
  const server = new McpServer(
    { name: "osint-desk", version: "0.1.0" },
    {
      instructions:
        "Live vessel positions from the Finnish Transport Infrastructure Agency AIS feed " +
        "(Digitraffic, CC BY 4.0). Positions are observed. Vessel names, destinations and " +
        "types are broadcast by the vessel itself and are not verified by anyone.",
    },
  );

  server.registerTool(
    "find_vessels_near",
    {
      title: "Find vessels near a position",
      // Four questions, in order: what it does, when to call it, when not to,
      // and what comes back. Stage 04 is where you learn what happens without
      // the third one.
      description:
        "List vessels currently reporting a position within a radius of a point in Finnish waters, " +
        "joined to the name, destination and type each vessel broadcasts about itself. " +
        "Use when the question is what is near a place right now. " +
        "Do NOT use to look up one known vessel by name or MMSI, and do NOT use for aircraft or for " +
        "any position outside Finnish coastal waters — this feed covers neither. " +
        `Returns at most ${MAX_ROWS} vessels, nearest first, each with distance in km, decoded ` +
        "navigational status, and a self_reported block holding every field the vessel supplied itself.",
      inputSchema: z
        .object({
          latitude: z.number().min(-90).max(90),
          longitude: z.number().min(-180).max(180),
          radius_km: z.number().min(1).max(500).default(25),
          limit: z.number().int().min(1).max(MAX_ROWS).default(10),
        })
        .strict(),
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: true },
    },
    async ({ latitude, longitude, radius_km: radiusKm, limit }) => {
      try {
        // The join the feed does not do for you: positions carry only an MMSI.
        const [locations, vessels] = await Promise.all([getJson(AIS_LOCATIONS), getJson(AIS_VESSELS)]);
        const byMmsi = new Map(vessels.map((v) => [v.mmsi, v]));

        const near = locations.features
          .map((f) => {
            const [lon, lat] = f.geometry.coordinates;
            return { p: f.properties, lat, lon, distance_km: km(latitude, longitude, lat, lon) };
          })
          .filter((v) => v.distance_km <= radiusKm)
          .sort((a, b) => a.distance_km - b.distance_km);

        const rows = near.slice(0, Math.min(limit, MAX_ROWS)).map(({ p, lat, lon, distance_km }) => {
          const meta = byMmsi.get(p.mmsi);
          return {
            mmsi: p.mmsi,
            distance_km: Number(distance_km.toFixed(2)),
            observed: { latitude: lat, longitude: lon, speed_over_ground_kn: p.sog, course_over_ground: p.cog,
                        navigational_status: NAV_STATUS[p.navStat] ?? `unmapped code ${p.navStat}`,
                        reported_at: new Date(p.timestampExternal).toISOString() },
            // Everything below is typed by whoever is aboard. Nothing checks it.
            self_reported: meta
              ? { name: meta.name?.trim() || null, destination: meta.destination?.trim() || null,
                  call_sign: meta.callSign?.trim() || null, ship_type: shipType(meta.shipType),
                  draught_m: meta.draught != null ? meta.draught / 10 : null }
              : null,
          };
        });

        const structuredContent = {
          source: "Finnish Transport Infrastructure Agency AIS via Digitraffic (CC BY 4.0)",
          queried_at: new Date().toISOString(),
          matched: near.length,
          returned: rows.length,
          truncated: near.length > rows.length,
          provenance: {
            observed: "position, speed, course and navigational status are received from the vessel's transponder",
            self_reported: "name, destination, call sign, ship type and draught are broadcast by the vessel and verified by nobody",
          },
          vessels: rows,
        };
        return { content: [{ type: "text", text: JSON.stringify(structuredContent, null, 2) }], structuredContent };
      } catch (error) {
        // Recoverable: hand the agent something it can act on rather than crashing.
        return {
          isError: true,
          content: [{ type: "text", text: `The AIS feed could not be read: ${error.message}` }],
          structuredContent: { error: "feed_unavailable", message: error.message },
        };
      }
    },
  );

  // ---------------------------------------------------------------------
  // YOUR TOOLS GO HERE. Two to five in total, including the one above.
  // Before you write one, say out loud whether it is a tool, a resource or a
  // prompt, and why it is not one of the other two.
  // ---------------------------------------------------------------------

  return server;
}

const isMain = process.argv[1] && process.argv[1].endsWith("server.mjs");
if (isMain) serveStdio(() => createDeskServer(), { legacy: "serve" });
