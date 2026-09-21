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

**Lab 01, Step 1: Missing ownership review**

**Task:** Filter the `owner` field to show blank values only.

**Method:** Used the column filter, cleared all selected values, selected only `(Blanks)`, and applied the filter.

**Why it matters:** A missing owner prevents clear accountability for cloud spend. This filter is a practical first step for identifying spend that needs ownership assignment before optimization or chargeback decisions.

**Conclusion:** When the owner is blank, the organization cannot clearly identify the person or team accountable for that resource's cost.

**Lab 01, Step 2: Missing cost-center review**

**Task:** Filter the `cost_center` field to show blank values only.

**Method:** Reset the prior filter, then used the `cost_center` column filter to select only `(Blanks)`.

**Result:** The filtered view isolated resources that have a business unit but no cost-center assignment.

**Conclusion:** Without a cost center, the organization cannot reliably allocate the resource's spend to the correct department for reporting or chargeback.

**Lab 01, Step 3: High-cost production review**

**Task:** Find production resources costing more than $500 per month.

**Method:** Filtered `environment` to `prod`, then applied the condition `monthly_cost` greater than `500`.

**Result:** 179 of 540 synthetic billing records met both conditions.

**Takeaway:** High cost is a review signal, not proof of waste. The next step is to investigate utilization, business purpose, and ownership before recommending a change.

**Operational safeguard:** Do not immediately shut down or resize a costly production resource. First confirm what it supports, whether it is appropriately utilized, how critical it is, and who owns the decision.

**Status:** Step 3 complete. Next, calculate total spend by business unit with `SUMIFS`.
