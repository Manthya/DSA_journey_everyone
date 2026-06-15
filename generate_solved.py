import re
import html
import os

SOLVED_MD = "solved.md"
SOLVED_HTML = "solved.html"


def parse_solved_md(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Split into blocks wherever a new question starts (e.g. "121. Title")
    blocks = re.split(r"\n(?=\d+\.)", content)

    questions = []
    for block in blocks:
        block = block.strip()
        if not block or not re.match(r"^\d+\.", block):
            continue

        lines = block.split("\n")
        title = lines[0].strip()

        tip = ""
        code_lines = []

        for line in lines[1:]:
            if re.match(r"^\s*tip\s*:", line, re.IGNORECASE):
                tip = re.sub(r"^\s*tip\s*:\s*", "", line, flags=re.IGNORECASE).strip()
            else:
                code_lines.append(line)

        # Strip leading/trailing blank lines from code block
        while code_lines and not code_lines[0].strip():
            code_lines.pop(0)
        while code_lines and not code_lines[-1].strip():
            code_lines.pop()

        questions.append({"title": title, "tip": tip, "code": "\n".join(code_lines)})

    return questions


def build_question_html(q, idx):
    title = html.escape(q["title"])
    tip_html = ""
    if q["tip"]:
        tip_html = f"""
        <div class="tip">
          <span class="tip-label">Tip</span>
          {html.escape(q["tip"])}
        </div>"""

    code_html = f"<pre><code>{html.escape(q['code'])}</code></pre>" if q["code"] else ""

    return f"""
  <div class="card">
    <div class="card-header">
      <span class="q-title">{title}</span>
      <button class="toggle-btn" onclick="toggle({idx})">Show Answer</button>
    </div>
    <div class="answer" id="ans-{idx}">
      {tip_html}
      {code_html}
    </div>
  </div>"""


def generate_html(questions):
    cards = "\n".join(build_question_html(q, i) for i, q in enumerate(questions))
    count = len(questions)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Solved Questions ({count})</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background: #0d1117;
      color: #c9d1d9;
      font-family: 'Segoe UI', system-ui, sans-serif;
      padding: 2rem;
    }}

    h1 {{
      font-size: 1.5rem;
      color: #58a6ff;
      margin-bottom: 1.5rem;
      border-bottom: 1px solid #21262d;
      padding-bottom: 0.6rem;
    }}

    .card {{
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 8px;
      margin-bottom: 0.6rem;
      overflow: hidden;
    }}

    .card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.75rem 1rem;
      gap: 1rem;
    }}

    .q-title {{
      font-size: 0.95rem;
      font-weight: 500;
      color: #e6edf3;
    }}

    .toggle-btn {{
      flex-shrink: 0;
      background: #21262d;
      border: 1px solid #30363d;
      color: #58a6ff;
      font-size: 0.75rem;
      font-weight: 600;
      padding: 0.28rem 0.8rem;
      border-radius: 5px;
      cursor: pointer;
      transition: background 0.15s, color 0.15s;
      white-space: nowrap;
    }}

    .toggle-btn:hover {{ background: #58a6ff; color: #0d1117; }}
    .toggle-btn.open  {{ background: #388bfd22; border-color: #58a6ff; color: #58a6ff; }}

    .answer {{
      display: none;
      padding: 0.9rem 1rem 1rem;
      border-top: 1px solid #21262d;
      background: #0d1117;
    }}

    .answer.visible {{ display: block; }}

    .tip {{
      font-size: 0.875rem;
      color: #c9d1d9;
      background: #f0883e18;
      border-left: 3px solid #f0883e;
      border-radius: 3px;
      padding: 0.45rem 0.7rem;
      margin-bottom: 0.85rem;
    }}

    .tip-label {{
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #f0883e;
      margin-right: 0.5rem;
    }}

    pre {{
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 6px;
      padding: 0.9rem 1rem;
      overflow-x: auto;
      font-size: 0.82rem;
      line-height: 1.65;
    }}

    code {{
      font-family: 'Fira Code', 'Cascadia Code', Consolas, monospace;
      color: #e6edf3;
    }}
  </style>
</head>
<body>

<h1>✅ Solved Questions &nbsp;<small style="font-size:0.85rem;color:#6e7681;">({count})</small></h1>

{cards}

<script>
  function toggle(idx) {{
    const ans = document.getElementById('ans-' + idx);
    const btn = ans.previousElementSibling.querySelector('.toggle-btn');
    const open = ans.classList.toggle('visible');
    btn.textContent = open ? 'Hide Answer' : 'Show Answer';
    btn.classList.toggle('open', open);
  }}
</script>

</body>
</html>"""


def main():
    if not os.path.exists(SOLVED_MD):
        print(f"'{SOLVED_MD}' not found.")
        return

    questions = parse_solved_md(SOLVED_MD)
    html_content = generate_html(questions)

    with open(SOLVED_HTML, "w") as f:
        f.write(html_content)

    print(f"Generated '{SOLVED_HTML}' with {len(questions)} question(s).")


if __name__ == "__main__":
    main()
