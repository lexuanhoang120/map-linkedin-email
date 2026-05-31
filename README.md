# LinkedIn Email Enrichment

<!-- > **Note:** Source code is not publicly available due to confidentiality restrictions. -->

## Highlights

- **50,000 emails** processed through authorized LinkedIn profile lookup
- **4,070 profiles matched** (8.1% match rate) with structured enrichment across profile, work, and education
- **2,041 profiles** with work-experience data and **1,560** with education data
- Privacy-aware pipeline with authorized session-based access — no credential sharing
- Extracted attributes support customer profiling, segmentation, and professional-background analytics

---

## Demo

### No Match

![Email no match demo](docs/no%20match.png)

### Matched

![Email match demo](docs/demo1.png)

---

## Results

*50,000 email input sample*

| Stage | Count | Rate |
|---|---:|---:|
| Emails checked | 50,000 | 100% |
| Matched to LinkedIn accounts | **4,070** | 8.1% |
| Profiles with work-experience data | 2,041 | 4.1% |
| Profiles with education data | 1,560 | 3.1% |

### Work Experience Profile

Most matched profiles had 1–2 listed experiences.

| Experiences | Profiles |
|---|---:|
| 1 | 1,306 |
| 2 | 205 |
| 3 | 161 |
| 4 | 114 |
| 5+ | 101 |

**Top job titles:** Student, Manager, Teacher, Project Manager, Engineer, Software Engineer, Accountant, Director, Developer, Architect.

Work end year was often missing — likely because many profiles list current positions.

### Education Profile

| Education Records | Profiles |
|---|---:|
| 1 | 1,226 |
| 2 | 230 |
| 3 | 73 |
| 4+ | 24 |

**Top fields:** Business Administration, Information Technology, Computer Science, Marketing, Accounting, HR Management, Finance, Mechanical Engineering.

Education date ranges were more complete than work-experience date ranges.

---

## What It Does

Given a list of customer emails, the pipeline answers:

- Which emails can be matched to LinkedIn profiles?
- What professional, education, and work-experience information is available?
- How complete is the collected profile data?
- Can the enriched information support customer segmentation?

### Information Extracted

| Category | Fields |
|---|---|
| **General Profile** | Display name, headline, summary, current company, location, LinkedIn URL, connection count, skills |
| **Work Experience** | Job title, company, start/end year, number of positions per profile |
| **Education** | School, degree, field of study, start/end year, number of education records per profile |

---

## Pipeline

```
Email sample
    ↓
Authorized profile lookup (Outlook → LinkedIn session)
    ↓
Classify result (matched / partial / no match / failed)
    ↓
Parse profile response into structured tables
    ↓
Normalize profile, work, and education data
    ↓
Aggregate results and evaluate data quality
```

---

## Quick Start

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Prepare input: resource/email.xlsx (column: email)
# Prepare account: resource/account.txt (outlook_email|password|recovery_email)

# Step 1: Generate authorized session
python 1_get_token_from_outlook.py
# → access_token.json

# Step 2: Match emails to LinkedIn profiles
python 2_email_in_linkedin.py
# → email_match_linkedin.json
```

Requires Chrome + ChromeDriver for the token collection step.

---

## Project Structure

```text
.
├── 1_get_token_from_outlook.py   # Authorized session generation
├── 2_email_in_linkedin.py        # Email-to-LinkedIn matching
├── requirements.txt
├── docs/
│   ├── no match.png
│   └── demo1.png
├── resource/                     # Local input files (not committed)
│   ├── account.txt
│   ├── email.xlsx
│   └── chromedriver
├── access_token.json             # Generated session (not committed)
├── email_match_linkedin.json     # Generated output (not committed)
└── README.md
```
