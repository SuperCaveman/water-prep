# Public Study Log

This is a curated record of hands-on cloud and FinOps study work. It documents objectives, attempts, feedback, and takeaways without reproducing private conversations, personal details, account information, or interview logistics.

## Session 1: Cloud Billing Dataset Orientation

**Objective:** Classify the fields in a synthetic multi-cloud billing dataset before building calculations.

**Why it matters:** Cloud-cost analysis combines business accountability with technical resource data. Correctly separating ownership, resource, usage, and cost fields makes later reporting, allocation, and investigation work more reliable.

**Tooling:** Google Sheets or another spreadsheet application that can open `.xlsx` files.

**Exercise:** Review the `Raw Billing` worksheet and assign each of its 16 fields to one of four groups:

1. Ownership and business context
2. Technical resource context
3. Usage and utilization
4. Financial and cost measures

**Attempt and feedback:** The first field reviewed was `account`. The initial attempt treated it as a spend value. Review clarified the distinction between an account label, which identifies a responsible billing scope, and `monthly_cost`, which contains the dollar amount. Therefore, `account` belongs to ownership and business context.

**Status:** In progress. Next, classify `usage_hours`.
