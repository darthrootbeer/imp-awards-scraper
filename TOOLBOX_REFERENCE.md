# TOOLBOX Reference

This project uses shared tools from the centralized TOOLBOX repository.

**Location**: `~/projects/TOOLBOX/`

**Quick Access**:
- Documentation: `~/projects/TOOLBOX/README.md`
- Quick Reference: `TOOLBOX_QUICK_REFERENCE.md` (in this project)
- Examples: `TOOLBOX_EXAMPLES.py` (in this project)
- Scripts: `~/projects/TOOLBOX/scripts/`
- Config: `~/projects/TOOLBOX/config/`

**Key Features**:
- Pushover notifications with project identifier (`vader/{project-name}`)
- Styled HTML emails with icon and project identifier
- Timestamp formatting: `format_timestamp()` → "Sat 2025-12-13 • 5:17p" (Eastern)
- Message formatting helpers: `format_message()` for best practices
- Config file support: `config/pushover.yaml` for defaults

**Setup Verification**:
```bash
~/projects/TOOLBOX/scripts/verify_toolbox_setup.sh
```

**Python Usage**:
```python
import sys
sys.path.append('../../TOOLBOX/python')
from pushover import send_pushover, format_message, format_timestamp
from emailer import send_email, send_styled_email, format_timestamp
```

See `TOOLBOX_QUICK_REFERENCE.md` for complete usage examples.
