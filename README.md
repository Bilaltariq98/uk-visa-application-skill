# uk-visa-application: a Claude Code skill

An agent skill that helps someone prepare a UK visa or immigration application with Claude, with a human making every decision. Claude interviews the applicant, builds an organised evidence pack, checks it against the **current** Home Office rules, drafts request letters and a cover letter, runs a GO / NO-GO preflight, and can guide a browser agent through the online form. It always stops before payment and submission.

The skill goes deepest on spouse/partner applications (Appendix FM / FM-SE), but the workflow works for any route.

> **Not legal advice.** Immigration rules, fees and thresholds change often. The skill makes Claude re-check gov.uk every session and refers judgement calls to an OISC-registered adviser or a solicitor. You remain responsible for every answer you submit.

## What it does

1. **Intake interview.** Claude asks probing questions in small batches, including easy-to-miss risks such as benefit claims made in the applicant's name.
2. **Workspace setup.** Numbered evidence folders, `requests/`, `submit/`, and a `.trash/` folder (files are moved there, never deleted).
3. **Document triage.** Downloaded files are handled safely, renamed with dates, filed, and flagged if they are weak or inconsistent.
4. **Gap analysis.** Each requirement is checked against freshly fetched official guidance.
5. **Request letters.** Drafts to employers, landlords/agents, councils and HMRC, written in your own tone.
6. **Cover letter.** One section per requirement, with open disclosure of any risks.
7. **Preflight** (`scripts/preflight.py`). Gives GO / NO-GO based on:
   - permission expiry
   - ID validity
   - how recently the rules were verified
   - required files
   - document freshness (e.g. 28-day payslips)
   - monthly series coverage
   - unfilled placeholders
   - open risks
8. **Form filling.** A browser agent follows `FORM_GUIDE.md`. It never pays or submits until the human types "submit".

## Freshness built in

- **Rules:** figures in `references/` are stamped with the date they were last checked and are treated as pointers, not answers. Preflight blocks if `rules_verified_on` in `case.json` is older than 14 days (configurable).
- **Documents:** filenames carry dates, and `case.json` sets the maximum age of each dated document. Preflight computes the "submit by" deadline.

## Install

```bash
git clone <this-repo-url> ~/.claude/skills/uk-visa-application
```

Then ask Claude Code something like *"Help me prepare my spouse visa extension"*. The skill triggers automatically.

To use the preflight on its own, copy `scripts/preflight.py` and `assets/case.example.json` (renamed to `case.json`) into `<workspace>/submit/`, edit the JSON, then run:

```bash
python3 submit/preflight.py            # GO = exit 0, NO-GO = exit 1
python3 submit/preflight.py --today 2027-01-05
python3 submit/preflight.py --selftest
```

Requires Python 3.8+ (stdlib only). Document triage uses `pdftotext`/`pdftoppm` (poppler), plus `sips` on macOS for HEIC.

## Layout

```
SKILL.md                       workflow and rules Claude follows
references/intake-questions.md interview question bank
references/partner-route.md    spouse/partner evidence map (re-verify!)
references/gotchas.md          traps seen in real applications
references/letter-templates.md request letter templates
scripts/preflight.py           GO / NO-GO check, configured by case.json
assets/case.example.json       example config
assets/FORM_GUIDE.template.md  browser-agent form guide template
```

## Privacy

Everything stays local. The skill tells Claude not to send applicant data to external services or copy it into reusable files. Don't commit a real `case.json` or any evidence to a fork of this repo.

## Contributing

Corrections to rules are very welcome. Please cite the gov.uk or Immigration Rules source and the date you checked it.
