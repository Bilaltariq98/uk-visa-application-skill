# <Route> online form: guide for the browser agent

Applicant: **<NAME AS ON PASSPORT>**. Sponsor/partner (if any): **<NAME>**. Human in charge: **<who approves>**.

`TBD` (and other placeholder markers in case.json) block the preflight. **CONFIRM** lines don't block it, but the agent must ask the human before answering.

Rules last verified against gov.uk on: **TBD** (also set `rules_verified_on` in case.json).

---

## Rules for the agent (obey all)

1. Run `python3 submit/preflight.py`. On **NO-GO**, stop, report the blockers, and don't open the form.
2. Never pay, accept the final declaration, or press the final submit. Stop at payment and wait until the human types "submit".
3. Never invent an answer. A question that isn't here, or is marked CONFIRM, means pause and ask.
4. Benefits / public funds, criminality, refusals, breaches, deception: always pause and confirm the wording, even if a draft is below.
5. Copy names, numbers and dates exactly as written here (passport spelling).
6. Upload only the files the preflight lists under "UPLOAD THESE FILES". Never upload from `.trash/`.
7. Screenshot each section. Record the application reference.
8. On timeout, sign back in and continue. Never start a second application.
9. Before entering any fee, compare it with the payment page. If it differs from this guide, pause and tell the human.

---

## 1. Start
- Start page (verify current URL on gov.uk): TBD
- Account email / phone: TBD

## 2. Applicant: personal details
| Question | Answer |
|---|---|
| Given / family names | TBD |
| Other names | TBD |
| Sex / DOB / place of birth | TBD |
| Nationality / other nationalities | TBD |
| Passport number, issue, expiry, authority | TBD |
| National Insurance number | TBD |

## 3. Contact and address history
| Address | From–to | Basis |
|---|---|---|
| TBD | | |

## 4. Immigration history
| Question | Answer |
|---|---|
| Current permission, valid from/until | TBD |
| Previous application reference | TBD |
| Arrival date / travel since | TBD |
| Refusals, overstaying, breaches | TBD |

## 5. Partner / sponsor (if applicable)
TBD

## 6. Children / dependants
TBD

## 7. Parents of the applicant
TBD

## 8. Financial requirement
| Question | Answer |
|---|---|
| Category / source | TBD |
| Employer, job, start date, type | TBD |
| Gross annual salary (and from when) | TBD |
| Threshold that applies (source + date verified) | TBD |

## 9. Accommodation
| Question | Answer |
|---|---|
| Type and rooms | TBD |
| Occupants (names, DOBs) | TBD |
| Space-standard calculation | TBD |

## 10. English language
TBD

## 11. Public funds
- Received any public funds? TBD
- CONFIRM: any "applied for / claimed" question. Draft wording: TBD

## 12. Character and debts
TBD

## 13. Fees (verified on TBD; recheck on the payment page)
- Application fee: TBD
- Immigration Health Surcharge: TBD
- Service level: TBD
- STOP before payment (rule 2).

## 14. After submission
- Save reference and confirmation email.
- Identity verification (app / UKVCAS): TBD
- Upload documents in preflight order.
