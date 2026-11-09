import csv, json, html, datetime

CSV_PATH = "/Users/moefx/Documents/JobHunt/tracker/applications.csv"
OUT_PATH = "/Users/moefx/Documents/JobHunt/dashboard/index.html"

with open(CSV_PATH, newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

status_order = ["interview_requested", "applied", "new", "skipped_other", "skipped_scam_risk", "rejected"]
status_colors = {
    "interview_requested": "#22c55e",
    "applied": "#3b82f6",
    "new": "#a3a3a3",
    "skipped_other": "#eab308",
    "skipped_scam_risk": "#ef4444",
    "rejected": "#71717a",
}

counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1

data_json = json.dumps(rows)
counts_json = json.dumps(counts)
colors_json = json.dumps(status_colors)
generated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

html_out = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Job Hunt Tracker — Muhammed Ragab</title>
<style>
  body {{ font-family: -apple-system, system-ui, sans-serif; background: #0f1117; color: #e5e7eb; margin: 0; padding: 24px; }}
  h1 {{ font-size: 22px; margin-bottom: 4px; }}
  .meta {{ color: #9ca3af; font-size: 13px; margin-bottom: 20px; }}
  .cards {{ display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 24px; }}
  .card {{ background: #1a1d29; border-radius: 10px; padding: 14px 18px; min-width: 120px; }}
  .card .n {{ font-size: 26px; font-weight: 700; }}
  .card .l {{ font-size: 12px; color: #9ca3af; text-transform: uppercase; letter-spacing: .04em; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ text-align: left; padding: 10px 8px; border-bottom: 2px solid #2a2e3f; color: #9ca3af; font-size: 11px; text-transform: uppercase; }}
  td {{ padding: 10px 8px; border-bottom: 1px solid #22263a; vertical-align: top; }}
  tr:hover {{ background: #161925; }}
  .badge {{ display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 11px; font-weight: 600; color: #0f1117; }}
  .notes {{ color: #9ca3af; max-width: 420px; }}
  .filterbar {{ margin-bottom: 14px; }}
  .filterbar button {{ background: #1a1d29; color: #e5e7eb; border: 1px solid #2a2e3f; border-radius: 6px; padding: 6px 12px; margin-right: 6px; cursor: pointer; font-size: 12px; }}
  .filterbar button.active {{ background: #3b82f6; border-color: #3b82f6; }}
  a {{ color: #60a5fa; }}
</style>
</head>
<body>
<h1>Job Hunt Tracker</h1>
<div class="meta">Generated {generated_at} &middot; {total} applications tracked &middot; data: tracker/applications.csv</div>

<div class="cards" id="cards"></div>
<div class="filterbar" id="filterbar"></div>
<table id="tbl">
  <thead>
    <tr>
      <th>Status</th><th>Job</th><th>Org / Country</th><th>Salary</th><th>Source</th><th>Dates</th><th>Notes</th>
    </tr>
  </thead>
  <tbody id="tbody"></tbody>
</table>

<script>
const rows = {data_json};
const colors = {colors_json};
let activeFilter = null;

function badge(status) {{
  const c = colors[status] || '#71717a';
  return `<span class="badge" style="background:${{c}}">${{status.replace(/_/g,' ')}}</span>`;
}}

function render() {{
  const tbody = document.getElementById('tbody');
  tbody.innerHTML = '';
  const filtered = activeFilter ? rows.filter(r => r.status === activeFilter) : rows;
  filtered.forEach(r => {{
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${{badge(r.status)}}</td>
      <td><b>${{r.job_title}}</b></td>
      <td>${{r.school_org}}<br><span style="color:#9ca3af">${{r.country}}</span></td>
      <td>${{r.salary_range || '-'}}</td>
      <td>${{r.source}}</td>
      <td style="font-size:11px;color:#9ca3af">found: ${{r.date_found||'-'}}<br>applied: ${{r.applied_date||'-'}}<br>follow-up: ${{r.follow_up_date||'-'}}</td>
      <td class="notes">${{r.notes||''}}</td>
    `;
    tbody.appendChild(tr);
  }});
}}

function renderCards() {{
  const counts = {{}};
  rows.forEach(r => counts[r.status] = (counts[r.status]||0)+1);
  const cardsEl = document.getElementById('cards');
  cardsEl.innerHTML = Object.entries(counts).map(([s,n]) =>
    `<div class="card"><div class="n" style="color:${{colors[s]||'#fff'}}">${{n}}</div><div class="l">${{s.replace(/_/g,' ')}}</div></div>`
  ).join('');
}}

function renderFilterbar() {{
  const counts = {{}};
  rows.forEach(r => counts[r.status] = (counts[r.status]||0)+1);
  const bar = document.getElementById('filterbar');
  let html = `<button data-f="" class="active">All (${{rows.length}})</button>`;
  Object.keys(counts).forEach(s => {{
    html += `<button data-f="${{s}}">${{s.replace(/_/g,' ')}} (${{counts[s]}})</button>`;
  }});
  bar.innerHTML = html;
  bar.querySelectorAll('button').forEach(b => {{
    b.addEventListener('click', () => {{
      activeFilter = b.dataset.f || null;
      bar.querySelectorAll('button').forEach(x => x.classList.remove('active'));
      b.classList.add('active');
      render();
    }});
  }});
}}

renderCards();
renderFilterbar();
render();
</script>
</body>
</html>
""".format(data_json=data_json, counts_json=counts_json, colors_json=colors_json, generated_at=generated_at, total=len(rows))

with open(OUT_PATH, "w") as f:
    f.write(html_out)
print("written", OUT_PATH, len(html_out), "bytes")
