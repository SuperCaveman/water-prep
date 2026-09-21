# SQL Lab 01 — Select and Filter

Use table cloud_billing.

1. Return the cloud_provider and monthly_cost columns. Limit the result to five rows.
2. Return production resources costing more than $500 per month.
3. Return the five highest monthly-cost resources, including provider, service, environment, and cost.
4. Join `cloud_billing` to `cost_centers` on `cost_center` to return the department and chargeback owner for a billing record.

For each result, explain what operational question it helps answer. Do not assume an expensive production resource is wasteful without validating purpose, utilization, and ownership.
