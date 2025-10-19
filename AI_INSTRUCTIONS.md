# AI Assistant Instructions (October 2025)

These guidelines help AI pair-programming tools (Cursor, GPT Codex, etc.)
work safely and consistently inside `imp-awards-scraper`.

## Project Context
- **Purpose**: Automate downloading the highest-resolution movie posters
  from IMP Awards, enforce genre/resolution rules, and optionally email
  digest updates.
- **Key entry points**:
  - `poster_downloader.py` – main CLI + scraping pipeline.
  - `email_sender.py` – email digest and thumbnail batching.
  - `genre_config.yaml` / `resolution_config.yaml` – user-tunable rules.
  - `movie_metadata.json` – persistent catalogue of movies (genres, release date, poster variants).
  - `scripts/install.py` / `scripts/run_email_digest.sh` – onboarding and daily automation helpers.
- **Virtual env**: use the checked-in `venv` (`venv/bin/python3`) when
  running scripts locally unless directed otherwise.

## Installation Overview (guide the user through this flow)
1. **Prerequisites**
   - Python 3.8 or newer.
   - Git (or download the ZIP).
   - TMDb API key (free at https://www.themoviedb.org/settings/api).
   - SMTP account capable of sending mail (Gmail app password recommended).
2. **Clone or download the repository**
   ```bash
   git clone https://github.com/darthrootbeer/imp-awards-scraper.git
   cd imp-awards-scraper
   ```
3. **Run the guided installer**
   ```bash
   python3 scripts/install.py
   ```
   - Creates/updates `venv`.
   - Installs dependencies via pip.
   - Prompts for TMDb key and SMTP settings, writes `.env`.
   - Ensures `movie_metadata.json` exists.
   - Generates `scripts/run_email_digest.sh`.
   - Offers to add a daily cron job (asks for time, page depth, test mode).
   - Mentions the user can rerun the installer any time to update credentials/scheduling.
4. **Manual fallback**
   - If the user prefers manual setup, guide them through `pip install -r requirements.txt`, creating `.env`, and optional scheduler entries.
5. **Validation**
   - Run `venv/bin/python3 poster_downloader.py --help` to confirm the CLI works.
   - Optional quick scrape: `venv/bin/python3 poster_downloader.py --latest --pages 1`.
   - Send a test digest (adds `[TEST]` prefix): `scripts/run_email_digest.sh --digest-pages 5 --digest-test`.

## Daily Automation Guidance
- `scripts/run_email_digest.sh` reads the virtualenv automatically and defaults to scanning five latest pages. Accepts CLI flags identical to the Python script (e.g., `--digest-pages 10`).
- Cron entry format (installed by the script): `${minute} ${hour} * * * /path/to/scripts/run_email_digest.sh --digest-pages 5`.
- For macOS users preferring launchd, adapt `QUICK_EMAIL_START.md` example but point to `scripts/run_email_digest.sh`.

## Workflow Expectations
1. **Stay incremental**  
   - Prefer focused changes with clear rationale.  
   - Mirror existing coding style (PEP 8, docstrings where helpful, light
     inline comments only for non-obvious logic).
2. **Keep automation-ready**  
   - Command-line modes must remain non-interactive when invoked with
     flags (`--latest`, `--year`, future digest flags).  
   - Preserve duplicate detection, genre filtering, and resolution
     priority guarantees.
3. **Configuration safety**  
   - Do not hard-code credentials. Respect `.env` loading and explain any
     new environment variables in `.env.example` + docs.  
   - Never touch `downloads/` contents in commits; treat as runtime data.
4. **Email digest features**  
   - Reuse `email_sender.EmailSender`; extend via dependency injection
     rather than rewriting.  
   - Track poster IDs/paths in JSON (e.g., `email_tracking.json`,
     prospective digest trackers) and keep file writes atomic.

## When Adding Features
- Update `README.md`, `EMAIL_SETUP.md`, `SUMMARY.md`, and any relevant
  quick-start docs with new flags or workflow changes.
- If behavior changes, bump `VERSION`, `__version__`, and append to
  `CHANGELOG.md` (use semantic versioning).
- Maintain backward compatibility for existing CLI arguments unless the
  change is coordinated across docs.

## Validation & Testing
- Prefer fast, deterministic checks. Examples:
  - `venv/bin/python3 poster_downloader.py --help`
  - Dry-run scrape logic with limited pages (catch HTML parsing issues).
  - For email features, use mock/stub flows; avoid sending real emails
    in CI or scripted tests.
- Note skipped tests or manual verification steps in the PR/commit
  description when automation is impractical.

## Commit & Review Conventions
- Use Conventional Commit prefixes (`feat:`, `fix:`, `chore:`, etc.).
- Group related changes in a single commit; avoid mixing refactors and
  feature work without explanation.
- Include concise rationale in commit bodies for significant changes
  (especially around scraping logic or email batching).

## Communication with Humans
- Surface risks first (e.g., rate limiting, TMDb quota, IMP markup
  changes).  
- Offer validation steps the user can run locally.  
- Keep responses concise, actionable, and reference file paths with line
  numbers when relevant (`poster_downloader.py:176` style).

Following these conventions ensures future AI agents can collaborate on
the project without corrupting its automation workflows.
