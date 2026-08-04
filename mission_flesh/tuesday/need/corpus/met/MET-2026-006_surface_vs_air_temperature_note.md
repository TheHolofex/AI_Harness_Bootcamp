# Surface Temperature and Air Temperature Are Not the Same Quantity: Technical Note

**Issued by:** Estate Works Section, Instrumentation Cell, Task Group MERIDIAN, Station Halberd
**Reference:** MET-2026-006
**Issue:** 2
**Date of issue:** 30 April 2026
**Supersedes:** MET-2026-006 Issue 1 (18 August 2025)
**Prepared by:** Okafor, B., Instrumentation Cell
**Distribution:** All users of the estate surface sensor export; Movement Desk; Estate Works file

**Classification:** TRAINING SYNTHETIC - EXERCISE NORTHWIND SHELF. All units, organisations, people, places and events in this document are invented.

## 1. Why this note exists

The Instrumentation Cell receives a steady stream of requests in which a surface
figure is asked for and an air figure is offered instead, or the reverse, on the
assumption that the two are close enough or that one can be adjusted into the
other. They are not close enough, no adjustment exists, and this note sets out
why.

No values appear in this note. Figures from the estate surface sensor network are
held in the estate surface sensor export, against the sensor identifier and
timestamp they belong to.

## 2. What each quantity is

**Air temperature** is the temperature of the air, measured by a sensor held in a
ventilated radiation screen at a standard height above short grass over open
ground, deliberately shielded from direct and reflected radiation and from the
influence of any nearby surface. The screen exists precisely to remove the
effects that surface temperature is a measurement of. Air temperature is designed
to be regionally representative: two properly sited screens some distance apart
will usually agree closely, which is what makes air temperature useful in
forecasts and in regional summaries.

**Surface temperature** is the temperature of a specific piece of material, at a
specific place, with the sensing face in the plane of the trafficked surface. It
is not shielded from anything. It is a measurement of the thermal state of that
material under whatever radiation, wind, shading, moisture and traffic it is
actually experiencing, and it is representative of nothing except itself. Two
surfaces a short distance apart can differ substantially, which is the whole
reason the estate network has eight sensors rather than one.

They are different physical quantities, measured by different methods, for
different purposes. They share a unit. Sharing a unit is not the same as being
interchangeable, and the shared unit is the reason the substitution keeps being
attempted.

## 3. What drives them apart

**Solar radiation.** A surface exposed to the sun absorbs radiation and heats
above the air moving over it. A shaded surface a few paces away does not. The
screen that houses an air sensor excludes this effect entirely. This is the
largest single cause of divergence and it operates only in daylight.

**Sky view and night-time radiative loss.** At night a surface with a clear view
of the sky radiates to space and can cool below the air temperature above it. A
surface under a cutting face, a tree line, a bridge soffit or a building has a
restricted sky view and cools less. The divergence at night therefore has the
opposite sign to the divergence by day, and it varies between sensors according
to what each of them can see.

**Material and thermal mass.** A thick concrete slab stores heat and changes
slowly; a thin dark bituminous layer over a light base changes quickly and
reaches further from the air temperature in both directions. Colour, texture and
reflectance all matter. Two surfaces in identical exposure but different
construction will not read alike.

**What is beneath.** A surface over solid ground is coupled to a large thermal
reservoir that resists change. A surface over a structural deck with air
underneath is not, and follows conditions much more closely because it can lose
and gain heat from both faces.

**Wind.** Air movement couples a surface to the air above it. In strong wind the
two quantities converge, sometimes closely. In still conditions they diverge, and
the divergence can be at its widest.

**Moisture.** A wet surface is held near the temperature of evaporation and is
substantially decoupled from what a dry surface alongside it is doing. A surface
that is wetted intermittently, as at a slipway apron, alternates between the two
regimes.

**Traffic and shading by objects.** A standing vehicle shades the surface beneath
and behind it and changes what the sensor is measuring for as long as it is
there. Air temperature is unaffected by any of this.

## 4. The consequences

**There is no offset.** The difference between surface and air temperature is not
a constant, is not a constant for a given site, and is not a constant for a given
site at a given time of day. It varies with cloud, sun angle, wind, wetness,
season and what happens to be parked nearby. Any rule of the form "add so much to
the air figure" is wrong, and it is wrong by an amount that changes from hour to
hour.

**The sign reverses.** Surface can be above air or below it, and which it is
depends mainly on whether the sun is on it. A correction fitted to daytime data
is not merely inaccurate at night; it points the wrong way.

**A forecast of one is not a forecast of the other.** Forecast air temperature is
a forecast of a screened, regionally representative quantity. It is not a
forecast of the state of any particular piece of surfacing, and it cannot be
turned into one without a surface energy model, site parameters and inputs the
forecast does not carry.

**Neither substitutes for the other in a record.** Where a document, a log or a
decision requires a surface figure, an air figure is not a degraded version of
it and not a conservative stand-in. It is a measurement of something else.

## 5. Standing instruction

Where the estate surface sensor network is the source specified, take the figure
from the estate surface sensor export, against the correct sensor identifier and
timestamp, and carry both with the value.

Where a surface figure is required and the relevant sensor is unavailable, say
that it is unavailable. Do not fill the gap with an air temperature, with a
figure from a different sensor, or with an adjustment of either. An acknowledged
absence can be worked around. A substituted figure looks like an answer and
cannot be told apart from one afterwards.
