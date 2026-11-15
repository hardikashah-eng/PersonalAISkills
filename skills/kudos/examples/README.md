# Kudos example

## bea-retry-fix: one fix, four versions

Bea (fictional) fixed a retry storm in PR #482. `note.json` holds:

- `body`: a direct message naming what she did, the difference, and the care behind it
- `channel_post`: the #kudos version (`share.py --channel slack --post`)
- `manager_note`: a note to her manager, so it counts at review time (`--manager`)
- `public_post`: a LinkedIn post in public terms, with no PR number, no
  internal detail, and Bea's consent recorded (`--channel linkedin`; checked
  with `safety_check.py --profile public`)

`outputs.txt` shows all four as printed by `share.py`.
