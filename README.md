# Water Prep

Hands-on technical interview preparation focused on cloud operations, FinOps, cloud billing analysis, Excel, SQL, chargeback/showback, and business reporting.

This repository uses **synthetic data only**. It is designed as a learning lab and does not contain proprietary Xylem data, internal pricing, or confidential information.

## Goal

Build practical fluency for an early-career cloud/FinOps technical interview by working through one consistent synthetic cloud-billing dataset from raw data to business decisions.

The learning path is deliberately ordered. We work one exercise at a time: attempt first, then receive feedback or a progressively stronger hint. This is a training lab, not a completed answer key.

1. **Excel FinOps Lab** — tables, filters, `SUMIFS`, `COUNTIFS`, `XLOOKUP`, PivotTables, charts, conditional formatting, and month-over-month analysis.
2. **SQL Cloud Billing Lab** — `SELECT`, `WHERE`, `ORDER BY`, aggregates, `GROUP BY`, `HAVING`, `CASE`, and joins.
3. **Chargeback & Showback Lab** — tagging, ownership, cost allocation, shared-cost allocation, showback, and chargeback.
4. **FinOps Investigation Lab** — investigate a cloud-cost spike, identify drivers, validate ownership, quantify savings, and recommend action.
5. **Dashboard & Mock Interview Lab** — build management-ready reporting and defend the analysis in technical interview scenarios.

## Instructor mode

For every Excel, SQL, Python, FinOps, and interview task:

- Receive one objective and a brief concept explanation.
- Attempt the work yourself before seeing a solution.
- Receive feedback on what is correct and what needs adjustment.
- Ask for a hint if needed; hints become more specific only when necessary.
- See a complete answer only after an attempt or an explicit request.

## Why these skills matter

- **Excel** turns raw billing data into clear stakeholder reporting.
- **FinOps** connects cloud use, financial accountability, and sensible optimization.
- **Showback and chargeback** make ownership and allocation decisions visible and defensible.
- **SQL and reporting** make recurring investigation faster and more reliable.
- **Cloud operations** ensures cost findings are validated safely before changes are made.

## Current starting materials

```text
water-prep/
├── README.md
└── water_prep_excel_lab.xlsx
    ├── Raw Billing
    ├── Cost Centers
    ├── Exercises
    └── Excel Reference
```

The remaining folders and lab materials will be added only when they are needed for the next learning phase:

```text
data/  exercises/  sql/  python/  docs/
```

## Synthetic dataset

The current workbook contains 540 synthetic records across three months of AWS, Azure, and GCP-style usage. Its raw-billing fields include:

- month
- cloud provider
- account
- business unit
- cost center
- chargeback owner
- environment
- service
- resource ID
- region
- owner
- usage hours
- monthly cost
- CPU utilization
- storage size
- tag completeness

It intentionally contains interview-style FinOps problems: underutilized compute, development resources running continuously, missing ownership/cost-center tags, idle storage, and month-over-month cost growth.

## Ground rules

- Do the exercise before looking for a shortcut.
- Explain *why* a result matters, not only how to calculate it.
- Do not assume that expensive means wasteful.
- Do not shut down or resize production resources without validation and an owner.
- Separate facts from estimates when calculating potential savings.
- Use the simplest tool that answers the business question clearly.

## Interview mental model

For cost investigations, use:

**Anomaly → Attribution → Ownership → Investigation → Recommendation → Approval → Action → Validation**

For operational troubleshooting, use:

**Scope → Recent changes → Metrics/logs → IAM → Network → Resource/application health → Remediation → Verify → Document**

## Progress checklist

- [ ] Excel fundamentals — Lab 01: dataset orientation
- [ ] SUMIFS / COUNTIFS
- [ ] XLOOKUP
- [ ] PivotTables and month-over-month analysis
- [ ] SQL fundamentals and aggregation
- [ ] SQL joins
- [ ] FinOps fundamentals and tagging
- [ ] Showback, chargeback, and shared-cost allocation
- [ ] Forecasting and variance
- [ ] Cost anomaly investigation
- [ ] Cost optimization
- [ ] Power BI reporting
- [ ] Cloud-operations troubleshooting
- [ ] Mock technical interview

## Setup

- Open `water_prep_excel_lab.xlsx` in Microsoft Excel.
- Start on `Raw Billing`; use `Exercises` only to record your own work.
- No cloud account, production data, or Xylem internal information is required.

## Core FinOps concepts

Cost visibility, tagging, attribution, allocation, showback, chargeback, shared-cost allocation, forecasting, variance, optimization, and governance will be learned through the same dataset.

## Interview lessons

State what changed, identify the likely owner and driver, distinguish facts from estimates, validate with the resource owner before action, and explain how you would measure the result afterward.

## Getting started

Start with `water_prep_excel_lab.xlsx`, beginning with the `Raw Billing` worksheet. The first task is to classify the dataset fields before doing any calculations.

Do not rush ahead. The point is to become comfortable doing the work yourself.
