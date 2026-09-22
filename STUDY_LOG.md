# Hands-On Study Portfolio

This is a curated record of hands-on cloud and FinOps study work. It documents completed exercises, methods, results, and operational takeaways without reproducing raw conversations, personal details, account information, or interview logistics.

## Interview Cram Sheet: Role-Aligned Priorities

Public postings describe this as a Cloud Operations, FinOps, and reporting role—not a generic AWS certification role. The work emphasizes actionable cost, utilization, operational-readiness, security, and performance dashboards; billing-data analysis; allocation, forecasting, showback, and chargeback; Excel; BI modernization; access requests; routine service support; documentation; stakeholder coordination; and on-call readiness. [Role listing](https://builtin.com/job/cloud-engineer/10913648) · [Matching posting](https://www.monster.com/job-openings/cloud-engineer-morrisville-nc--ad8553a2-e6f5-478f-8b38-1a6c4115aa6a)

### Top FinOps and cloud questions

**1. “Cloud spend increased 30%. Walk me through your investigation.”**

> “I would validate the variance in Cost Explorer, break it down by provider, account, service, region, environment, business unit, and owner, then identify the largest deltas. I would use CloudWatch or Datadog to validate whether usage, traffic, or a deployment explains the change. I would confirm findings with the owner, recommend an approved action if appropriate, and measure workload health and realized savings afterward.”

**Key rule:** Expensive is a review signal, not proof of waste.

**2. “Explain showback, chargeback, and allocation of a shared cost.”**

> “Showback makes a team’s cloud cost visible; chargeback assigns it to that team’s cost center or budget. Direct costs use ownership tags. For shared costs, I would use the most relevant usage driver—such as log volume for monitoring or GB for storage. If usage data is not available, I would use a transparent temporary proxy, such as direct-spend share, and validate the method with Finance and Engineering.”

**Likely follow-up:** For unallocated spend, quantify it, prioritize high-cost untagged resources, identify ownership, correct tags, and add governance or automation to prevent recurrence.

**3. “What would you put in a cloud cost/performance dashboard?”**

Use **SCODA**: **Spend, Change, Owner, Driver, Action.**

> “I would show total spend and forecast; month-over-month variance; business unit, cost center, and owner; top provider, service, and environment drivers; and an action queue for unallocated spend, anomalies, and optimization reviews. I would add selected performance, security, and operational-readiness signals where they explain cost or risk.”

For AWS, use Cost Explorer or a Cost and Usage Report for billing data, then CloudWatch or Datadog for performance context. [AWS Cost Explorer](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-default-reports.html) · [AWS CUR](https://docs.aws.amazon.com/cur/latest/userguide/what-is-cur.html)

### Top Excel questions

**1. “Build a report showing monthly spend by business unit.”**

> “Create a PivotTable with `business_unit` in Rows, `month` in Columns, and `SUM of monthly_cost` in Values. Add provider, service, or environment for drill-down.”

**2. “How would you calculate spend for one business unit and find its chargeback owner?”**

```excel
=SUMIFS('Raw Billing'!M:M,'Raw Billing'!D:D,"Operations")
=XLOOKUP("CC-300",'Cost Centers'!A:A,'Cost Centers'!C:C)
```

`SUMIFS` totals costs that match criteria; `XLOOKUP` maps billing metadata, such as a cost center, to ownership information.

**3. “How would you find and prevent poor billing-data quality?”**

> “Filter for blank owner and cost-center values, quantify unallocated spend, and prioritize the highest-cost gaps. Use data-validation dropdowns for fields such as environment, business unit, and cost center so future entries follow a controlled standard.”

### Additional role signals

- Dashboards should cover **cost, utilization, performance, security, and readiness**—not cost alone.
- For access requests and service issues: identify the principal, action, resource, and error; use least privilege; test, document, and escalate when appropriate.
- For BI modernization, use: **Source → clean → model → visualize → refresh.**
- Be ready to discuss Jira/documentation, Finance and Engineering collaboration, recurring deadlines, and stakeholder communication.
- For an AI proof of concept: define the business problem, data/security constraints, cost and success measures, run a limited POC, document findings, and scale only after validation.
- Know basic multi-cloud equivalents without overstating depth: AWS Account / Azure Subscription / GCP Project; EC2 / Azure Virtual Machines / Google Compute Engine; S3 / Azure Blob Storage / Google Cloud Storage.

**Core message:** Turn cloud data into a validated, owner-approved business decision.

## Session 1: Cloud Billing Dataset Orientation

**Objective:** Classify the fields in a synthetic multi-cloud billing dataset before building calculations.

**Why it matters:** Cloud-cost analysis combines business accountability with technical resource data. Correctly separating ownership, resource, usage, and cost fields makes later reporting, allocation, and investigation work more reliable.

**Tooling:** Google Sheets or another spreadsheet application that can open `.xlsx` files.

**Exercise:** Review the `Raw Billing` worksheet and assign each of its 16 fields to one of four groups:

1. Ownership and business context
2. Technical resource context
3. Usage and utilization
4. Financial and cost measures

**Outcome:** `account` identifies a responsible billing scope, while `monthly_cost` contains the dollar amount. Therefore, `account` belongs to ownership and business context.

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

**Lab 01, Step 4: Total spend by business unit with `SUMIFS`**

**Task:** Calculate total `monthly_cost` for the Operations business unit.

**Formula:** `=SUMIFS('Raw Billing'!M:M,'Raw Billing'!D:D,"Operations")`

**Result:** `$51,674.36`

**How it works:** The formula adds values from column M (`monthly_cost`) only when the matching value in column D (`business_unit`) is `Operations`.

**Lab 01, Step 5: Count long-running non-production resources with `COUNTIFS`**

**Task:** Count resources that are not in production and have more than 650 usage hours.

**Formula:** `=COUNTIFS('Raw Billing'!G:G,"<>prod",'Raw Billing'!L:L,">650")`

**Result:** `52` resources

**How it works:** `COUNTIFS` counts rows where `environment` is not `prod` and `usage_hours` exceeds 650. The `<>` operator means “not equal to.”

**Takeaway:** Long-running non-production resources are candidates for investigation because development or test workloads may be able to follow a schedule. Validate their purpose and ownership before making a change.

**Lab 01, Step 6: Map a cost center with `XLOOKUP`**

**Task:** Return the chargeback owner associated with cost center `CC-300`.

**Formula:** `=XLOOKUP("CC-300",'Cost Centers'!A:A,'Cost Centers'!C:C)`

**Result:** `Marcus Reed`

**How it works:** `XLOOKUP` searches column A (`cost_center`) on the `Cost Centers` sheet for `CC-300`, then returns the corresponding value from column C (`chargeback_owner`).

**Takeaway:** A lookup table translates billing metadata into accountable business information, which supports accurate showback or chargeback reporting.

**Lab 01, Step 7: PivotTable for monthly cost by business unit and month**

**Task:** Create a decision-friendly summary of spend over time by business unit.

**Configuration:**

- **Rows:** `business_unit`
- **Columns:** `month`
- **Values:** `SUM of monthly_cost`

**How it works:** The PivotTable groups the synthetic billing records by business unit and month, then totals monthly cost for every intersection.

**Takeaway:** This report makes it easier to spot spend trends, compare departments, and drill into unusual changes before deciding on an optimization action.

**Evidence:** ![Lab 01 PivotTable showing monthly cost by business unit and month](evidence/lab-01-pivottable.png)

**Lab 01, Step 8: PivotTable drill-down by cloud provider and service**

**Task:** Extend the business-unit cost trend report so a reviewer can isolate provider and service-level drivers.

**Configuration:** Added `cloud_provider` and `service` beneath `business_unit` in the PivotTable Rows area; retained `month` as Columns and `SUM of monthly_cost` as Values.

**How it works:** The row hierarchy supports progressive analysis: business unit → cloud provider → service. A double-click on a PivotTable value can also create a detail sheet containing the source rows behind that total.

**Takeaway:** A cost trend is only the starting point. Drill-down makes it possible to trace a variance to the provider and service producing it before engaging the accountable owner.

**Lab 01, Step 9: Month-over-month total spend change**

**Task:** Calculate the percent change in total spend from June 2026 to July 2026.

**Formula:** `=(SUMIFS('Raw Billing'!M:M,'Raw Billing'!A:A,DATE(2026,7,1))-SUMIFS('Raw Billing'!M:M,'Raw Billing'!A:A,DATE(2026,6,1)))/SUMIFS('Raw Billing'!M:M,'Raw Billing'!A:A,DATE(2026,6,1))`

**Result:** `-8.27%`

**How it works:** The formula sums monthly cost for each month, subtracts June from July, then divides by June to express the change as a percentage. It references raw billing data so the result remains stable even if a PivotTable drill-down changes the layout of totals.

**Takeaway:** Total spend fell 8.27% from June to July. The next operational question is what provider, service, or business-unit changes explain that variance; the percentage alone does not establish the cause.

**Lab 02 setup: Local SQL Cloud Billing Lab**

**Environment:** Created a local SQLite database and a read-only query prompt from the same 540 synthetic billing records used in Lab 01.

**Validation:** The database contains 540 records and reconciles to total monthly cost of `$227,448.97`.

**Outcome:** Lab 01 established a spreadsheet-based foundation for cost attribution, ownership analysis, and trend reporting.

**Lab 02, Step 1: Select billing columns**

**Task:** Return a small sample of cloud provider and monthly cost values from the local synthetic billing table.

**Query:** `SELECT cloud_provider, monthly_cost FROM cloud_billing LIMIT 5;`

**Result:** Returned five rows successfully.

**How it works:** `SELECT` chooses the columns, `FROM` names the table, and `LIMIT 5` keeps the result to a quick sample.


**Lab 02, Step 2: Filter costly production resources**

**Task:** Return production resources costing more than $500 per month.

**Query:** `SELECT cloud_provider, service, monthly_cost FROM cloud_billing WHERE environment = 'prod' AND monthly_cost > 500 LIMIT 5;`

**Result:** Returned five qualifying records from the synthetic billing data.

**How it works:** `WHERE` applies row-level conditions. `AND` requires both conditions to be true: the resource must be in `prod` and have a monthly cost above 500.

**Takeaway:** These records are investigation candidates, not proof of waste. Confirm business purpose, utilization, criticality, and owner before proposing a production change.


**Lab 02, Step 3: Rank highest-cost resources**

**Task:** Return the five highest monthly-cost resources across the synthetic billing dataset.

**Query:** `SELECT cloud_provider, service, environment, monthly_cost FROM cloud_billing ORDER BY monthly_cost DESC LIMIT 5;`

**Result:** The top five records were all production resources. The highest was AWS EC2 at `$1,401.10` per month.

**How it works:** `ORDER BY monthly_cost DESC` sorts from highest to lowest. `LIMIT 5` returns only the first five rows.

**Takeaway:** Ranking focuses investigation on the largest cost drivers. It does not determine whether a resource should be changed; production workloads require owner and operational validation first.


**Lab 02, Step 4: Aggregate spend by business unit**

**Task:** Calculate total monthly cost for each business unit and rank them from largest to smallest.

**Query:** `SELECT business_unit, SUM(monthly_cost) AS total_monthly_cost FROM cloud_billing GROUP BY business_unit ORDER BY total_monthly_cost DESC;`

**Result:** Operations was highest at `$51,674.36`, followed by Engineering at `$49,786.22`.

**How it works:** `SUM(monthly_cost)` adds cost values. `GROUP BY business_unit` produces one total per business unit. The alias `total_monthly_cost` gives the calculated column a readable name.

**Cross-check:** The Operations total matches the `SUMIFS` result from the spreadsheet lab.


**Lab 02, Step 5: Filter business-unit totals with `HAVING`**

**Task:** Identify business units with total spend above `$45,000`.

**Query:** `SELECT business_unit, SUM(monthly_cost) AS total_monthly_cost FROM cloud_billing GROUP BY business_unit HAVING SUM(monthly_cost) > 45000 ORDER BY total_monthly_cost DESC;`

**Result:** Operations (`$51,674.36`) and Engineering (`$49,786.22`) met the threshold.

**How it works:** `WHERE` filters source rows before aggregation; `HAVING` filters grouped results after `SUM` has calculated each business unit's total.


**Lab 02, Step 6: Classify review candidates with `CASE`**

**Task:** Apply review labels to costly resources and long-running non-production resources.

**Query pattern:** `CASE WHEN ... THEN ... WHEN ... THEN ... ELSE ... END AS review_status`

**Result:** The ten highest-cost records were all labeled `Review high cost` because each exceeded `$1,000` per month.

**How it works:** `CASE` provides ordered conditional logic in SQL. The first matching `WHEN` supplies the label, so the sequence of rules is meaningful.

**Takeaway:** A review label prioritizes analysis. It is not an instruction to change a production workload without validating its purpose, utilization, and owner.


**Lab 02, Step 7: Map billing records with a SQL `JOIN`**

**Task:** Attach department and chargeback-owner information to billing resources with cost center `CC-300`.

**Query:** `SELECT b.resource_id, b.cost_center, c.department_name, c.chargeback_owner FROM cloud_billing AS b JOIN cost_centers AS c ON b.cost_center = c.cost_center WHERE b.cost_center = 'CC-300' LIMIT 5;`

**Result:** Each returned resource mapped to Operations and chargeback owner Marcus Reed.

**How it works:** `JOIN` combines rows from `cloud_billing` and `cost_centers` where their `cost_center` values match. `b` and `c` are short aliases for the tables.

**Cross-check:** This is the SQL equivalent of the spreadsheet XLOOKUP that mapped `CC-300` to its chargeback owner.

**Outcome:** Lab 02 established a SQL foundation for sampling, filtering, ranking, aggregation, classification, and ownership lookup.

**Lab 03, Step 1: Showback, chargeback, and shared-cost allocation**

**Scenario:** Allocate a `$10,000` shared cloud-platform cost using each business unit's share of direct cloud spend.

**Example:** Operations represented `22.72%` of direct spend, so its allocated share was `$2,271.91`.

**Key distinction:** Showback reports the allocated amount to a team for visibility and accountability. Chargeback assigns that amount to the team's budget or cost center.

**Interview explanation:** “We allocated the shared cost based on each business unit's share of direct cloud spend. That is a consistent, transparent proxy for use; we publish the rule through showback and validate it with owners before applying chargeback.”


**Lab 03, Step 2: Identify a monthly cost-variance driver**

**Task:** Compare service-level cost from June to July and rank the largest increases.

**Result:** EBS had the largest increase, rising from `$5,418.98` in June to `$12,074.49` in July: a `$6,655.51` increase. CloudFront was second, increasing `$2,899.32`.

**Interpretation:** EBS is the leading candidate for investigation. A cost increase alone does not prove waste or establish savings.


**Lab 03, Step 3: Attribute the EBS variance**

**Result:** Finance on AWS, owned by Jamie Park, had the largest EBS increase at `$2,020.62`. Engineering/AWS increased `$1,823.48`; Sales/AWS added `$1,768.92` of new EBS spend.

**Interpretation:** The variance now has accountable business areas and owners. The next step is resource-level investigation, not an immediate optimization recommendation.


**Lab 03, Step 4: Inspect Finance/AWS EBS resources**

**Facts observed:** The largest July resource cost was a production volume (`res-00227`) at `$692.03`. A development volume (`res-00232`) ran `730` hours, stored `2,991 GB`, and cost `$341.32`.

**Interpretation:** The development volume is a candidate to review for scheduling or retention. Production volumes require owner, application, utilization, and resilience validation before any proposed change.


**Lab 03, Step 5: Split the EBS variance by environment**

**Result:** Finance/AWS production EBS increased `$1,415.33` from June to July. Development EBS was new in July at `$605.29`.

**Recommendation framing:** Investigate production growth with the owner and application context first. Separately, review development volumes for schedule, retention, and deletion eligibility under the applicable policy.

**Safeguard:** Neither amount is validated savings until the owner confirms the workload purpose and change path.

**Outcome:** Lab 03 demonstrated transparent allocation, cost-variance attribution, and the safeguards required before recommending storage optimization.

**Lab 03, Step 6: Storage safeguards for optimization**

**EBS:** Elastic Block Store is AWS block storage, similar to a virtual disk attached to an EC2 instance. Its storage cost can continue after an EC2 instance is stopped while the volume remains.

**Retention:** A defined period for keeping data or backups before deletion. Review whether a development EBS volume is attached, needed, backed up, or subject to a retention requirement before any removal.

**S3 distinction:** S3 is object storage for files in buckets, while EBS is block storage for server-attached volumes.

**Safeguard:** Never infer that an EBS volume is safe to delete solely because it is costly or associated with development.

**Lab 04, Step 1: Cloud-operations incident triage**

**Initial triage:** Confirm scope before remediation: production versus non-production, start time, affected users and regions, and recent changes.

**Evidence before action:** Review error rate, latency, load-balancer target health, application logs, and deployment history before restarting servers or changing configuration.

**Why it matters:** A restart can mask the symptom and introduce a new change, making the original incident harder to diagnose.


**Lab 04, Step 2: Load-balancer target health diagnosis**

**Scenario:** The load balancer is reachable but returns 503 because its targets are unhealthy.

**Check order:** Inspect target-group health status and its reason code, then validate health-check path and port, security-group reachability, application process/logs, and recent deployment changes.

**Reason-code guide:** A 404 suggests a health-check path or application-route mismatch. A timeout or connection refusal points to port, security group, service process, or network reachability. A 5xx indicates an application-level failure response.


**Lab 04, Step 3: IAM AccessDenied troubleshooting**

**First checks:** Identify the calling IAM principal, denied API action, target resource, and the policy evaluation path before changing permissions.

**EC2-to-S3 example:** Inspect the IAM role attached to the EC2 instance for `s3:GetObject` on the required bucket/object path. If it already allows access, inspect the bucket policy, service control policy, permission boundary or session policy, and KMS key permission for encrypted objects.

**Safeguard:** Do not attach broad administrator access as a shortcut. An explicit deny overrides an allow; use the smallest permission change that addresses the verified failure.

**Outcome:** Lab 04 established an evidence-first approach to incident triage, load-balancer health diagnosis, and least-privilege IAM troubleshooting.

**Lab 05, Technical Interview Response Frameworks**

**Cost variance:** Verify the dashboard change, then attribute it by provider, service, account, business unit, and owner. Do not turn off or resize resources merely because spend increased.

**Load balancer 503:** Inspect target-group health and its reason code before checking health-check configuration, security groups, application logs, and recent deployments.

**EC2-to-S3 AccessDenied:** Start with the EC2 instance role, denied action, and requested object path. Then inspect bucket policy, organization controls, permission boundaries, session policies, and KMS permissions as applicable.

**Outcome:** Lab 05 consolidated concise, evidence-based explanations for cost variance, load-balancer, and IAM troubleshooting scenarios.
