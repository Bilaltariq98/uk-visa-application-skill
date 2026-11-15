<div align="center">

# 🇬🇧 uk-visa-application

**An open [Agent Skill](https://agentskills.io) for preparing a UK visa or immigration application with an AI agent. You make the decisions; the agent does the legwork.**

![Agent Skill](https://img.shields.io/badge/Agent%20Skill-open%20format-6E56CF)
![Python](https://img.shields.io/badge/python-3.8%2B%20stdlib-3776AB)
![Status](https://img.shields.io/badge/status-beta-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

```bash
npx skills add bilaltariq98/uk-visa-application-skill
```

Works with Claude Code, Cursor, Codex, Gemini CLI, Copilot, OpenCode and other agents that support `SKILL.md`.

</div>

> [!WARNING]
> **This is not legal advice.** Immigration rules, fees and thresholds change several times a year. The skill makes the agent re-check gov.uk every session and refers judgement calls to an [OISC-registered adviser](https://www.gov.uk/find-an-immigration-adviser) or a solicitor. You are responsible for every answer you submit.

---

## Contents

- [What it does](#what-it-does)
- [Freshness is built in](#freshness-is-built-in)
- [Installation](#installation)
- [Usage](#usage)
- [The preflight check](#the-preflight-check)
- [Safety guardrails](#safety-guardrails)
- [Repository layout](#repository-layout)
- [Contributing](#contributing)

---

## What it does

The agent works through eight phases with you, asking questions at each step rather than guessing.

| # | Phase | What happens |
|:-:|---|---|
| 1 | **Intake interview** | The agent asks questions in small batches: route, expiry, people, addresses, income, housing, English, history, and **benefits** (including claims where payments were opted out, which people often miss). |
| 2 | **Workspace** | The agent creates numbered evidence folders, `requests/`, `submit/`, and a `.trash/` folder (files are moved there, never deleted). |
| 3 | **Document triage** | The agent handles each downloaded file safely, renames it `YYYY-MM-DD <What> - <Issuer> - <Person>`, files it, and flags spelling mismatches, missing signatures or out-of-date documents. |
| 4 | **Gap analysis** | The agent fetches the current official rules and maps each requirement to a status: ✅ have, ⚠️ weak, ❌ missing. |
| 5 | **Request letters** | The agent drafts letters to your employer, landlord or letting agent, council and HMRC, **in your own tone** (paste an example email). |
| 6 | **Cover letter** | The agent writes one section per requirement, each pointing to its evidence, and discloses any risks openly. |
| 7 | **Preflight** | A GO / NO-GO script checks expiry, IDs, files, document freshness, placeholders and open risks. |
| 8 | **Form filling** | The agent takes over the browser (Playwright MCP, Chrome DevTools MCP or computer use): it fills each page from `FORM_GUIDE.md`, verifies, screenshots, logs, and uploads the evidence. You sign in, handle 2FA and enter payment details; it **never pays or submits until you type `submit`**. |

The skill covers spouse/partner routes in most depth (Appendix FM / FM-SE). The workflow itself works for any route.

## Freshness is built in

Out-of-date information is the most common way a well-prepared application fails. The skill guards against two kinds:

| Risk | How the skill handles it |
|---|---|
| 📜 **Stale rules** (fees, thresholds, English levels, form wording) | Figures in `references/` are stamped "last verified" and treated as *what to look up*, not answers. The agent must fetch gov.uk or the Immigration Rules in the session and record the source and date. The preflight **blocks** if `rules_verified_on` is older than 14 days (configurable). |
| 📄 **Stale documents** (e.g. payslips and bank statements older than 28 days) | Filenames carry dates, and `case.json` sets a maximum age for each kind of dated document. The preflight works out the deadline, and the agent tells you a concrete **"submit by"** date and what to re-download if you miss it. |

## Installation

Use the open [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
# Interactive: pick your agent(s) and the install scope
npx skills add bilaltariq98/uk-visa-application-skill

# Global (user-level), for every project
npx skills add bilaltariq98/uk-visa-application-skill -g

# A specific agent only, without prompts
npx skills add bilaltariq98/uk-visa-application-skill -a claude-code -g -y

# Preview without installing
npx skills add bilaltariq98/uk-visa-application-skill --list
```

<details>
<summary><b>Manual install (no Node)</b></summary>

Copy `skills/uk-visa-application/` into your agent's skills directory. For example:

```bash
git clone https://github.com/bilaltariq98/uk-visa-application-skill.git
cp -r uk-visa-application-skill/skills/uk-visa-application ~/.claude/skills/   # Claude Code
```

</details>

To update or remove it later, run `npx skills update` or `npx skills remove uk-visa-application`.

## Usage

Just describe your situation. The skill triggers on its own:

```text
My wife's spouse visa expires in March. Help me get the extension together.
```

```text
Which payslips and bank statements do I upload for an FLR(M) application?
```

The agent will interview you, set up a workspace folder, and guide you from there. You can drop documents into the folders at any point, and the agent will triage them.

**Requirements:** Python 3.8+ (stdlib only). For document triage you also need `poppler` (`pdftotext` and `pdftoppm`); on macOS, `sips` handles HEIC photos.

## The preflight check

`preflight.py` reads all its settings from `submit/case.json`, so you never need to edit the script.

```bash
python3 submit/preflight.py                      # exit 0 = GO, exit 1 = NO-GO
python3 submit/preflight.py --today 2027-01-05   # simulate a future date
python3 submit/preflight.py --selftest           # check the logic
```

<details>
<summary><b>Example output</b></summary>

```text
Date checked: 2026-11-15. Permission expires 2027-01-31 (77 days left).

RESULT: NO-GO

BLOCKERS:
  - Rules/fees last verified never. Re-check gov.uk and set rules_verified_on (max 14 days).
  - Missing: Employer letter (03 Financial, name containing 'Employer letter').
  - Monthly payslips: missing 2026-07.
  - Unfilled: 06 Cover letter/cover-letter-draft.md:66: TBD (date of signing)
  - Open risk: Benefit claim in applicant's name. Get adviser view first.
```

</details>

<details>
<summary><b>What it checks</b></summary>

| Check | `case.json` key |
|---|---|
| Current permission not expired; a warning when it is close | `leave_expires`, `warn_days_left` |
| Rules re-verified recently | `rules_verified_on`, `rules_max_age_days` |
| Passports and IDs valid | `ids` |
| Required and recommended files present | `required`, `recommended` |
| Newest dated document within its maximum age | `fresh` |
| Consecutive monthly series (e.g. 6 payslips), each covered by a statement | `series` |
| No `TBD` or other placeholders left in drafts | `placeholder_files`, `placeholder_markers` |
| Open risks cleared | `open_risks` |

See [`case.example.json`](skills/uk-visa-application/assets/case.example.json) for a full spouse-extension example.

</details>

## Safety guardrails

- 🛑 **No payment, declaration or submission** without an explicit human `submit`.
- 🙋 **No invented answers.** Anything not in the guide, or marked `CONFIRM`, makes the agent pause and ask.
- ⚖️ **Sensitive questions always pause**, even when the guide has a draft answer: benefits, criminality, refusals, breaches.
- 🔒 **Data stays local.** The agent doesn't send your data to external services or copy it into reusable files.
- 🧪 **Downloads are treated as untrusted.** The agent processes them in temporary folders, checks the real file type, and runs Python with `-I`.
- 🗑️ **Nothing is deleted.** Superseded files go to `.trash/`.

## Repository layout

Standard [Agent Skills](https://agentskills.io/specification) layout, so `npx skills` discovers it under `skills/`:

```text
.
└── skills/uk-visa-application/
    ├── SKILL.md                 # frontmatter + the workflow the agent follows
    ├── references/
    │   ├── intake-questions.md  # interview question bank
    │   ├── partner-route.md     # spouse/partner evidence map (re-verify!)
    │   ├── gotchas.md           # traps seen in real applications
    │   ├── letter-templates.md  # employer, landlord, council, HMRC letters
    │   └── browser-agent.md     # how the agent drives the form and uploads
    ├── scripts/preflight.py     # GO / NO-GO check
    └── assets/
        ├── case.example.json    # example preflight config
        └── FORM_GUIDE.template.md
```

## Contributing

Rule corrections and new route guides (Skilled Worker, ILR, student, etc.) are very welcome. When you correct a rule, **cite the gov.uk or Immigration Rules source and the date you checked it**.

> [!CAUTION]
> Never commit a real `case.json`, cover letter or any evidence to a fork. They contain personal immigration data.

## License

[MIT](LICENSE)
