# Last Count closing desk for movement W-9

South Store supplies oral rehydration salts to Clinic R-12 on movement W-9.

The requirement line names the usable quantity. The decision time is 2026-10-16T18:00:00Z. All times in the packet are UTC. Quantity units are sachets.

A line is in destination custody only when movement, clinic, and lot family match the task, the snapshot is current (effective_at <= decision_time < valid_until), and receipt_status is DESTINATION.

A line contributes to usable quantity only when it is also RELEASED and CONFIRMED.

Unknown state on a current matching line forces HOLD. Held or unconfirmed lines in custody remain explicit zero-usable.

A closure document never substitutes for a quality release or clinic confirmation. Supersession applies only between matching movement/clinic/family records issued by the decision time. Report every closure as current-context-only, superseded, wrong-family, or future.

This packet is class review only. It does not authorize a real movement, a public posting, a dispatch, or any real custody decision. Named course coordinators only. There is no public notice.

The package must name purpose, bounds (desk, hours, audience, class-only limit), inputs, controls, run/check/stop/restore commands, strongest evidence, and next owner.
