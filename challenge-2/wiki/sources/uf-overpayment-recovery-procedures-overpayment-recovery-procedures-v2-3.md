---
source_id: "UF-OVERPAYMENT-RECOVERY-PROCEDURES-V2-3"
title: "Overpayment Recovery Procedures v2.3"
aliases:
  - "UF-OVERPAYMENT-RECOVERY-PROCEDURES-V2-3"
  - "Overpayment Recovery Procedures v2.3"
  - "Overpayment_Recovery_Procedures_v2.3"
source_path: "../../unstructured_files/Overpayment_Recovery_Procedures_v2.3.xlsx"
source_format: "xlsx"
document_type: "spreadsheet"
department: "DWP"
owner: null
status: "unknown"
version: null
publication_date: null
last_updated: null
audience: []
topics:
  - "housing-benefit"
  - "overpayment-recovery"
supersedes: []
related_sources: []
tags:
  - "source"
  - "challenge-2"
  - "xlsx"
  - "unknown"
  - "housing-benefit"
  - "overpayment-recovery"
extraction:
  method: "openpyxl-workbook"
  quality: "high"
  warnings: []
sensitivity:
  contains_personal_data: false
  classification: null
---

# Overpayment Recovery Procedures v2.3
## Summary

- Source: [Overpayment_Recovery_Procedures_v2.3.xlsx](../../unstructured_files/Overpayment_Recovery_Procedures_v2.3.xlsx)
- Extraction: `openpyxl-workbook` with `high` quality.
- Extract: Worksheet: Recovery Rates DWP Overpayment Recovery Procedures — Version 2.3 --- --- --- --- --- Owner: Debt Management Team \ November 2023 Benefit type Standard recovery rate Maximum recovery rate Hardship rate Notes Universal Credit 15% of standard allowance 25% of standard allowance 5% of standard allowance Deducted at source from ongoing UC payments Jobseeker's Allowance £11.10 per week £22.20 per week £3.70 per week Fixed amounts regardless of benefit rate Employment and Support Allowance £11.10 per week £22.20 per week £3.70 per week Same rates as JSA State Pension 15% of weekly pension 25% of weekly pension 5% of weekly pension...

## Metadata

| Field | Value |
| --- | --- |
| Source ID | UF-OVERPAYMENT-RECOVERY-PROCEDURES-V2-3 |
| Title | Overpayment Recovery Procedures v2.3 |
| Raw source | [Overpayment_Recovery_Procedures_v2.3.xlsx](../../unstructured_files/Overpayment_Recovery_Procedures_v2.3.xlsx) |
| Format | xlsx |
| Document type | spreadsheet |
| Department | DWP |
| Owner |  |
| Status | unknown |
| Version |  |
| Publication date |  |
| Last updated |  |
| Audience |  |
| Topics | housing-benefit, overpayment-recovery |
| SHA-256 | ab4d55947ec2df65a1cd38281eeddf2f9841259fe2979207d8cfa654ead19c12 |

## Navigation

- Topic: [Housing Benefit](../topics/housing-benefit.md)
- Topic: [Overpayment Recovery](../topics/overpayment-recovery.md)
- Entity: [Department For Work And Pensions](../entities/dwp.md)
- Entity: [HM Revenue And Customs](../entities/hmrc.md)
- Entity: [Local Authorities](../entities/local-authorities.md)

## Extracted Content

## Worksheet: Recovery Rates

| DWP Overpayment Recovery Procedures — Version 2.3 |  |  |  |  |
| --- | --- | --- | --- | --- |
| Owner: Debt Management Team \| November 2023 |  |  |  |  |
| Benefit type | Standard recovery rate | Maximum recovery rate | Hardship rate | Notes |
| Universal Credit | 15% of standard allowance | 25% of standard allowance | 5% of standard allowance | Deducted at source from ongoing UC payments |
| Jobseeker's Allowance | £11.10 per week | £22.20 per week | £3.70 per week | Fixed amounts regardless of benefit rate |
| Employment and Support Allowance | £11.10 per week | £22.20 per week | £3.70 per week | Same rates as JSA |
| State Pension | 15% of weekly pension | 25% of weekly pension | 5% of weekly pension |  |
| Pension Credit | £11.10 per week | £22.20 per week | £3.70 per week |  |
| Housing Benefit | Varies by LA | Varies by LA | Varies by LA | Recovered by the local authority, not DWP |
| PIP / DLA | Cannot be recovered from PIP/DLA directly |  |  | Must use another benefit or direct recovery |
| Child Benefit | Cannot be recovered from CB directly |  |  | Recovery via HMRC |
| Tax Credits |  |  |  | HMRC responsibility — not DWP |

## Worksheet: Escalation Thresholds

| Debt value | Action | Authority level | Timescale |
| --- | --- | --- | --- |
| £0 – £65 | Write off (below cost of recovery) | Team Leader | Immediate |
| £65.01 – £500 | Standard recovery from benefits | Decision Maker | Within 28 days of overpayment decision |
| £501 – £5,000 | Standard recovery + direct earnings attachment if no benefit in payment | HEO | Within 28 days |
| £5,001 – £10,000 | Above + consider civil court action | SEO | Review at 90 days if not recovered |
| £10,001 – £50,000 | Above + mandatory referral to Debt Enforcement | Grade 7 | Review at 60 days |
| £50,001 – £100,000 | Senior management review + potential fraud referral | G6 | Immediate review |
| Over £100,000 | Director approval required for recovery strategy | SCS1 | Immediate |
| Over £1m |  | Director General + referral to HMT | Immediate |
| [NOTE: The threshold at £65 was set in 2009 and has never been uprated. In real terms this is approximately £45 in 2009 prices. A review was recommended by the NAO in 2019 but has not been actioned.] |  |  |  |
| [KNOWN ERROR: The £1m threshold row is missing the 'Action' column text. It should read: 'Full recovery strategy and ministerial briefing'. This has been reported but not yet fixed in the published version.] |  |  |  |

## Worksheet: Fraud vs Non-Fraud

| Type | Definition | Recovery approach | Limitation period |
| --- | --- | --- | --- |
| Fraud (civil) | Claimant knowingly provided false information | Maximum recovery rate + civil penalty (50% of overpayment, min £350, max £5,000) | 6 years from date of overpayment decision |
| Fraud (criminal) | As above but referred for prosecution | Compensation order via courts + ongoing recovery | 6 years from date of conviction |
| Claimant error | Claimant failed to report a change of circumstances but without fraudulent intent | Standard recovery rate | 6 years from overpayment decision |
| Official error | DWP made a mistake in calculating the benefit | Recovery only where claimant could reasonably have been expected to know they were being overpaid | 6 years — but see note below |
| Technical | System error resulting in overpayment | Case-by-case assessment | No fixed policy — legal advice required |
| [IMPORTANT: The limitation period for recovery of official error overpayments is contentious. DWP's legal position is that the 6-year limit applies, but Upper Tribunal decisions in 2022 and 2023 have cast doubt on this. Await outcome of Court of Appeal case expected Q2 2024 before relying on this table.] |  |  |  |

## Worksheet: Payment Methods

| Method | Minimum amount | Notes |
| --- | --- | --- |
| Deduction from ongoing benefit | N/A | Preferred method — automatic |
| Direct Debit | £1 per month | Set up via Debt Management helpline |
| Standing Order | £1 per month |  |
| Online payment (GOV.UK Pay) | £5 | go.to/repay-benefit-overpayment |
| Telephone payment (card) | £5 | Via Debt Management helpline: 0800 XXX XXXX |
| Cheque | £5 | Payable to 'DWP Debt Management' — note: cheques being phased out, target removal date December 2024 |
| Direct Earnings Attachment | N/A | Employer deduction — no court order needed for benefit debts |
| Court order (County Court Judgment) | N/A | Last resort — requires legal authorisation |

## Worksheet: Contact

| Debt Management Helpline: 0800 XXX XXXX |
| --- |
| Monday to Friday, 08:00 – 18:00 |
| Email: debt.management@dwp.gov.uk |
| This document was last updated in November 2023. Recovery rates for UC are updated each April in line with the standard allowance. JSA/ESA/PC fixed rates are updated annually — the rates shown here are 2023-24 rates. |

## Raw Metadata

| Field | Value |
| --- | --- |
| created | 2026-04-14T08:54:51 |
| creator | openpyxl |
| exif_AppVersion | 3.1 |
| exif_Application | Microsoft Excel Compatible / Openpyxl 3.1.5 |
| exif_CreateDate | 2026:04:14 08:54:51Z |
| exif_Creator | openpyxl |
| exif_Directory | /Users/crpage/repos/ai-engineering-lab-hackathon-london-2026/challenge-2/unstructured_files |
| exif_ExifToolVersion | 13.5 |
| exif_FileAccessDate | 2026:04:16 03:33:03+01:00 |
| exif_FileInodeChangeDate | 2026:04:16 03:32:22+01:00 |
| exif_FileModifyDate | 2026:04:16 03:32:22+01:00 |
| exif_FileName | Overpayment_Recovery_Procedures_v2.3.xlsx |
| exif_FilePermissions | -rw-r--r-- |
| exif_FileSize | 10 kB |
| exif_FileType | XLSX |
| exif_FileTypeExtension | xlsx |
| exif_MIMEType | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet |
| exif_ModifyDate | 2026:04:14 08:54:51Z |
| exif_ZipBitFlag | 0 |
| exif_ZipCRC | 0x484dc746 |
| exif_ZipCompressedSize | 149 |
| exif_ZipCompression | Deflated |
| exif_ZipFileName | docProps/app.xml |
| exif_ZipModifyDate | 2026:04:14 08:54:50 |
| exif_ZipRequiredVersion | 20 |
| exif_ZipUncompressedSize | 205 |
| modified | 2026-04-14T08:54:51 |

## Related Notes

- [Knowledge base index](../index.md)
- [Lint report](../lint-report.md)
