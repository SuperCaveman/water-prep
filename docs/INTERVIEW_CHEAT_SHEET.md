# Cloud Engineer and FinOps Interview Cheat Sheet

## Cost investigation

Use this sequence:

```text
Anomaly → Attribution → Ownership → Investigation → Recommendation → Approval → Action → Validation
```

- Verify the period, amount, and baseline.
- Attribute the change by business unit, account, provider, service, environment, and resource.
- Identify the accountable owner.
- Separate facts from estimates.
- Do not stop, delete, or resize a production resource before owner and operational validation.
- Measure the result after an approved change.

Example: “I would verify the cost change, drill into the provider, service, account, and business unit to identify the driver and owner, validate the operational purpose, and only then present an approved recommendation with a measurable outcome.”

## FinOps allocation

- **Showback:** reports cost to the responsible team.
- **Chargeback:** assigns cost to that team’s budget or cost center.
- For shared cost, prefer a transparent allocation rule that reflects actual use when possible.
- Examples: logging by data-ingestion volume; a shared platform by an agreed usage metric; a shared service by direct-spend share when it is a reasonable proxy.

## SQL patterns

```sql
-- Inspect a small sample
SELECT cloud_provider, monthly_cost FROM cloud_billing LIMIT 5;

-- Filter rows
SELECT * FROM cloud_billing
WHERE environment = 'prod' AND monthly_cost > 500;

-- Aggregate like a PivotTable
SELECT business_unit, SUM(monthly_cost) AS total_monthly_cost
FROM cloud_billing
GROUP BY business_unit
ORDER BY total_monthly_cost DESC;

-- Filter grouped totals
... GROUP BY business_unit HAVING SUM(monthly_cost) > 45000;

-- Map a billing record to ownership information
SELECT b.resource_id, c.department_name, c.chargeback_owner
FROM cloud_billing AS b
JOIN cost_centers AS c ON b.cost_center = c.cost_center;
```

- `WHERE` filters rows before aggregation.
- `HAVING` filters grouped results after aggregation.
- `CASE` applies ordered conditional labels.
- `JOIN` is the SQL equivalent of a spreadsheet lookup.
- Use `IS NULL`, not `= NULL`, for missing values.

## Storage and optimization

- **EBS:** AWS Elastic Block Store, block storage similar to a virtual disk attached to EC2.
- **S3:** object storage for files in buckets.
- Stopping an EC2 instance does not necessarily stop EBS storage charges.
- Retention means how long data or backups must be kept before deletion.
- For a potentially unused development volume, validate attachment, data need, backup/retention requirement, and owner approval before deletion.

## Incident response

Use this sequence:

```text
Scope → Recent changes → Metrics/logs → IAM → Network → Resource/application health → Remediate → Verify → Document
```

- Scope production versus non-production, start time, affected users/regions, and recent changes.
- Inspect evidence before restarting servers or changing configuration.
- A load balancer 503 with unhealthy targets: inspect target-group reason codes, health-check path/port, security groups, application process/logs, and recent deployments.
- Health-check 404: likely route or health-check path mismatch.
- Timeout/connection refused: investigate port, security group, application process, or network reachability.
- `AccessDenied`: identify the principal, denied action, and resource before changing permissions. Use least privilege; inspect bucket policy, organization controls, boundaries, session policies, and KMS as applicable.

## Reporting

A decision-ready cost dashboard should answer:

1. How much are we spending?
2. Is spend rising or falling?
3. Which business unit, provider, or service drives the variance?
4. What needs review or action?

Use total spend, month-over-month change, business-unit/provider/service drill-down, ownership, and unallocated cost as the core views.
