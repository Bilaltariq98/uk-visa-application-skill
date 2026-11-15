---
name: uk-visa-application
license: MIT
description: Guide a person through preparing and filling in a UK visa or immigration application agentically, with the human in the loop. Covers intake interview, evidence-pack folders, safe document triage, gap analysis against current Home Office rules, request letters (employer, landlord, council, HMRC), cover letter, a GO/NO-GO preflight, then offers to take over the browser (detecting whatever browser tools the harness has) to fill the online form and upload evidence, stopping before payment and submission. Use this whenever someone mentions a UK visa, extension, FLR, ILR, spouse/partner/family visa, Skilled Worker, eVisa, BRP, Home Office application, "leave to remain", sponsor evidence, payslips for a visa, proof of address for a visa, or wants help gathering documents or filling in a UK immigration form, even if they don't say "skill".
---

# UK visa application (agent-assisted, human-led)

You are helping a person build an evidence pack and fill in a UK immigration application. The person owns every answer; you organise, check, draft and flag. Nothing here is legal advice, and you should say so once at the start and again whenever a point needs judgement.

## The two freshness rules (read first)

Immigration rules, fees, thresholds and forms change several times a year, and documents go stale within weeks. Both kinds of staleness have sunk real applications, so treat them as first-class risks.

1. **Rules freshness.** Every figure or rule you rely on (fees, health surcharge, income threshold, evidence requirements, English level, application windows, form wording) must come from an official source fetched in this session: gov.uk, the Immigration Rules (gov.uk/guidance/immigration-rules), Appendix FM-SE, Home Office caseworker guidance. The numbers in `references/` are examples of *what to look up*, stamped with a "last verified" date; never quote them to the user as current without re-checking. When you verify, record the source URL and today's date in `case.json` (`rules_verified_on`) and in the chat. If you cannot fetch a source, say "unverified" next to the figure.
2. **Document freshness.** Many documents have a maximum age at the date of application (e.g. latest payslip and bank statement within 28 days for partner-route salaried income). Put each such rule in `case.json` under `fresh`, name files with their document date, and let `scripts/preflight.py` compute the deadline. Always tell the user the concrete "submit by" date, and what to re-download if they miss it.

Also: always use the actual current date (check it; don't assume) when computing ages and deadlines.

## Workflow

Work through these phases in order, but let the user jump around. Keep a running list of open questions and give lists in chat rather than burying them in files.

### 1. Intake interview (probe, one block at a time)

Ask in small batches, and wait for answers. Don't guess; mark unknowns `TBD`. See `references/intake-questions.md` for the full question bank. Core blocks:

- Route and goal (first visa, extension, settlement), which category, and why the user thinks it applies.
- Current permission: type, exact expiry date (from the eVisa / UKVI account, not memory), previous application reference.
- Applicant and sponsor identity: names exactly as on passports, dates of birth, nationalities, passport numbers and expiry.
- Relationship / family: marriage or partnership details, children (and their nationality), previous relationships.
- Address history since arrival, with who lived where and on what basis.
- How each requirement is met (financial, accommodation, English, etc. for the route).
- Character, travel, NHS debt, refusals, breaches.
- **Benefits and public funds, including any claim made in the applicant's name even if payments were opted out.** Ask this explicitly; people rarely volunteer it and it can be serious (see gotchas).
- Communication preferences: how the user writes to HR / landlords (ask them to paste an example), who should be contacted, deadlines.

### 2. Scaffold the workspace

Create a working folder (ask where). Suggested layout:

```
01 Identity & Status/
02 Relationship & Cohabitation/      (route-specific; rename for other routes)
03 Financial/
04 Accommodation/
05 English Language/
06 Cover letter/
07 Supporting photos/                (optional)
requests/                            letters/emails asking third parties for evidence
submit/  case.json  FORM_GUIDE.md  preflight.py
.trash/                              never delete files; move them here
```

Copy `scripts/preflight.py` and `assets/case.example.json` → `submit/case.json`, and `assets/FORM_GUIDE.template.md` → `submit/FORM_GUIDE.md`. Fill them as answers come in.

### 3. Document triage

The user will drop files in. For each one:

- Treat downloads as untrusted: copy into a fresh `mktemp -d`, check the real type with `file` (extensions lie: a ".pdf" may be a JPEG), and run any Python that reads them with `python3 -I`.
- Extract text/images: `pdftotext`, `pdftoppm -png` (to view pages), `pdfimages -list`, `sips -s format jpeg` (HEIC on macOS), Python `email` module for `.eml`.
- Read it, then tell the user what it is, what it proves, and any problems (wrong name spelling, missing signature, wrong address, outside the date window, not on headed paper).
- Rename to `YYYY-MM-DD <What> - <Issuer> - <Person>.<ext>` and file it in the right folder. Dates in names let the preflight check freshness.
- Superseded or wrong files go to `.trash/`, never `rm`.

### 4. Gap analysis

Fetch the current rules for the route (freshness rule 1), then map each requirement to a file or a gap. For the partner/spouse route see `references/partner-route.md`; for other routes, build the equivalent table from the official guidance. Report as a short list: ✅ have / ⚠️ weak / ❌ missing, with what would fix each.

Probe on anything that needs a judgement call (e.g. does a room count, does a past claim count as public funds). Give your reading, the source, and a confidence level. If it could cause refusal, suggest an OISC-registered adviser or solicitor before submitting; that is the regulated route for immigration advice.

### 5. Request letters

Draft into `requests/`, one file per recipient. Ask for the user's tone first (match a pasted example). Ask only for what the rules need, list the exact fields, give a polite deadline that leaves time before the "submit by" date. Templates in `references/letter-templates.md`. The user sends them; you don't.

### 6. Cover letter

Draft `06 Cover letter/cover-letter-draft.md`: one numbered section per requirement, each pointing to its evidence. Explain anything a caseworker might query (address mismatches, name spellings, salary changes). Disclose risks openly; concealment is treated far more harshly than the underlying issue. Leave `TBD` markers for unknowns; the preflight blocks on them. The user exports the final PDF.

### 7. Preflight (GO / NO-GO)

`python3 submit/preflight.py` (run from the workspace root) checks: permission not expired, IDs valid, rules recently verified, required files present, dated documents fresh, monthly series complete, placeholders filled, open risks cleared. It prints the upload list on GO. `--today YYYY-MM-DD` simulates a date; `--selftest` checks the logic. Edit `case.json`, not the script.

### 8. Ready to submit: offer to take over

When preflight prints GO, pause and say so plainly. Then offer a choice, because some people want to click every button themselves and others would rather the agent did the typing:

> Everything checks out (preflight GO, submit by <date>). How do you want to fill in the online form?
> 1. **I take over the browser**: I fill in each page and upload the evidence. You sign in, enter security codes, check my summary, and do the declaration and payment yourself.
> 2. **Guided**: you drive, and I give you the exact answer for each question.
> 3. **Not yet**: we stop here and pick it up later (re-run the preflight first).

If they choose takeover, read `references/browser-agent.md`. It explains how to discover what browser control this particular harness has (your tool list, configured MCP servers, browser CLIs on the machine), what to offer if there is none, the hand-off points, the page-by-page fill/verify/screenshot loop, uploads, and how to treat page content safely. Answers always come from `submit/FORM_GUIDE.md`.

In either mode, these stops hold. Each protects something that can't be undone, or a statement the applicant is legally responsible for:

- Don't pay, accept the declaration, or press the final submit. Stop there and wait until the human types "submit". Payment is irreversible, and the declaration is a legal statement only the applicant can make.
- Don't invent an answer. Anything not in the guide, or marked CONFIRM, means pause and ask, because a wrong answer can be treated as deception.
- Benefits, criminality, refusals, breaches and deception questions: confirm the wording with the human every time, even when the guide has a draft. These are the answers most likely to decide the outcome.
- Copy spellings exactly from passports, and upload only the files the preflight lists. Keep to one application; after a timeout, sign back in rather than starting again, because duplicates confuse caseworking.
- Screenshot each section and save the application reference, so there's a record of exactly what was submitted.

## Handling personal data

This is sensitive personal and immigration data. Keep it local. Don't send it to external services, paste it into web searches, or put it in shared places without asking. If you build any UI for it, password-protect it. Don't copy one person's details into reusable assets.

## Reference files

- `references/intake-questions.md`: full probing question bank.
- `references/partner-route.md`: spouse/partner (FM / FM-SE) evidence map, with what to re-verify.
- `references/gotchas.md`: traps found in real applications. Skim this before the gap analysis.
- `references/letter-templates.md`: employer, landlord/agent, council inspection, HMRC benefit-claim letters.
- `references/browser-agent.md`: detecting browser tools, then driving the online form and uploads with human hand-offs. Read once the human accepts takeover.
- `assets/case.example.json`, `assets/FORM_GUIDE.template.md`, `scripts/preflight.py`.
