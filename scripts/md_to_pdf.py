#!/usr/bin/env python3
"""Convert docs/HACKATHON_SUBMISSION.md to PDF via HTML (xhtml2pdf)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    try:
        import markdown
        from xhtml2pdf import pisa
    except ImportError:
        print("Install: pip install markdown xhtml2pdf", file=sys.stderr)
        return 1

    md_path = ROOT / "docs" / "HACKATHON_SUBMISSION.md"
    pdf_path = ROOT / "docs" / "HACKATHON_SUBMISSION.pdf"
    if len(sys.argv) > 1:
        md_path = Path(sys.argv[1])
        pdf_path = md_path.with_suffix(".pdf")

    text = md_path.read_text(encoding="utf-8")
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "nl2br"],
    )
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
@page {{ size: A4; margin: 2cm; }}
body {{ font-family: Helvetica, Arial, sans-serif; font-size: 10pt; line-height: 1.4; color: #111; }}
h1 {{ font-size: 16pt; margin-top: 18pt; }}
h2 {{ font-size: 13pt; margin-top: 14pt; border-bottom: 1px solid #ccc; }}
h3 {{ font-size: 11pt; margin-top: 10pt; }}
table {{ border-collapse: collapse; width: 100%; margin: 10pt 0; font-size: 9pt; }}
th, td {{ border: 1px solid #444; padding: 5pt; vertical-align: top; }}
th {{ background: #eee; }}
code, pre {{ font-family: Courier, monospace; font-size: 8.5pt; background: #f5f5f5; }}
pre {{ padding: 8pt; white-space: pre-wrap; }}
hr {{ border: none; border-top: 1px solid #ccc; margin: 16pt 0; }}
</style>
</head>
<body>
{body}
</body>
</html>"""

    with pdf_path.open("wb") as out:
        status = pisa.CreatePDF(html.encode("utf-8"), dest=out, encoding="utf-8")
    if status.err:
        print(f"PDF errors: {status.err}", file=sys.stderr)
        return 1
    print(f"Wrote {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
