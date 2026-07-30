# Ops notes (synthetic)

- Roles are **case-insensitive**. Desk staff type `Admin` and `Clerk` in tickets.
- Empty amount fields should **fail closed** — never become zero dollars.
- Discounts above 100% must be rejected by the service, not accepted as negative prices.
- Last incident: a clerk paste of `percent=150` produced a credit instead of a charge. Ticket still open.
