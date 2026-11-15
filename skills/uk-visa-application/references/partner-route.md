# Partner / spouse route (Appendix FM + FM-SE): evidence map

**Last verified: November 2026. Re-verify every figure and rule below against gov.uk and the Immigration Rules before relying on it** (see SKILL.md, freshness rule 1). Items here tell you *what to check*, not the current answer.

Sources to fetch:
- gov.uk/uk-family-visa (and the extend / partner sub-pages)
- gov.uk/guidance/immigration-rules → Appendix FM, Appendix FM-SE, Part Suitability
- gov.uk/government/publications/public-funds (Public funds guidance)
- Fees: gov.uk "Home Office immigration and nationality fees"; IHS: gov.uk/healthcare-immigration-application/how-much-pay

## Timing
- Check when an extension may be made and whether remaining leave carries over. Don't tell people they must wait until a fixed number of days before expiry unless the current guidance says so.
- Applying before expiry usually keeps current conditions while pending (section 3C). Verify.

## Financial requirement
- Which threshold applies? It depends on when the person was first granted on this route (transitional provisions exist). Look up the current threshold *and* any transitional rule, then ask the user which applies to them.
- Category A (salaried, same employer 6+ months) per FM-SE (verify current wording):
  - Payslips covering the last 6 months.
  - Personal bank statements for the same period showing each net salary payment.
  - Letter from employer confirming: employment, gross annual salary, length of employment, period over which paid the salary relied on, type of employment (permanent/fixed/agency). Previous salary is not required.
  - The most recent payslip and statement must be no older than a set number of days at application (has been 28). Put this in `case.json` → `fresh`.
- Other categories (B: under 6 months; C/D savings; E/F self-employed; pension; exemption via disability benefits) each have their own evidence lists. Fetch FM-SE.

## Accommodation
- Must be adequate, owned or occupied exclusively by the family (at least one room), and not overcrowded under the Housing Act 1985 Part X.
- Space standard (s.326; verify):
  - Room standard: people of opposite sex aged 10+ who aren't partners must not have to share a sleeping room.
  - Persons count: under 1 = 0, 1–9 = 0.5, 10+ = 1.
  - Rooms count: bedrooms and living rooms normally used as such (kitchens and bathrooms excluded). Table I (rooms → persons): 1→2, 2→3, 3→5, 4→7.5, 5+→2 per room.
  - Room size (Table II): ≥110 sq ft = 2, 90–110 = 1.5, 70–90 = 1, 50–70 = 0.5, <50 = 0.
  - Ambiguous rooms (conservatory, unheated rooms): exclude them if the house passes without them, and say so in the cover letter.
- Evidence: tenancy agreement or title, council tax bill, and optionally a landlord letter or a council property inspection report. Inspections are optional; skip them if the numbers clearly pass.

## Relationship and cohabitation
- Marriage certificate (plus certified translation).
- Evidence of living together across the period: documents addressed to both partners at each address. Spread them over time.
- Children's birth certificates.

## English
- Level required depends on the stage (A1 first grant, A2 extension, B1 settlement; verify). Evidence: approved test, degree taught in English plus Ecctis/UK ENIC, or nationality/age/disability exemption. An earlier qualification at a higher level may still count; check.

## Public funds
- Partner leave normally carries "no recourse to public funds". Fetch the current public funds list. Child Benefit is on it.
- A claim in the applicant's name (even opted out of payment) may be treated as a breach. See gotchas.

## Identity and ID check
- After submission the applicant usually proves identity through the ID Check app or a UKVCAS appointment. Verify the current process.
