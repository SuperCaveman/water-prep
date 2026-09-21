# SQL Cloud Billing Lab

This lab uses the same 540 synthetic billing records as the spreadsheet exercise. It runs locally with Python's built-in SQLite support. No account, installation, or cloud data is required.

## Start the practice prompt

From the repository root:

```powershell
python sql/run_query.py
```

Type a SELECT query, press Enter, and type exit when finished. The prompt permits read-only SQL only.

## Table

cloud_billing

The columns match the spreadsheet: month, cloud_provider, account, business_unit, cost_center, chargeback_owner, environment, service, resource_id, region, owner, usage_hours, monthly_cost, cpu_utilization_pct, storage_gb, and tags_complete.

A second lookup table, `cost_centers`, contains `cost_center`, `department_name`, and `chargeback_owner` for JOIN practice.

## Lab sequence

1. Select columns and limit results.
2. Filter with WHERE.
3. Sort with ORDER BY.
4. Aggregate with SUM, COUNT, and GROUP BY.
5. Filter aggregated results with HAVING.
6. Classify results with CASE and connect lookup tables with JOIN.
