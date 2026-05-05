from pathlib import Path
from typing import Dict


def _format_rate(value: float) -> str:
    return f"{round(value * 100)}%"


def _build_table(title: str, rows: list[tuple]) -> str:
    if not rows:
        return f"""
        <section class="panel">
            <h2>{title}</h2>
            <p class="muted">No data available.</p>
        </section>
        """

    table_rows = "\n".join(
        f"<tr><td>{name}</td><td>{count}</td></tr>"
        for name, count in rows
    )

    return f"""
    <section class="panel">
        <h2>{title}</h2>
        <table>
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Count</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </section>
    """


def build_dashboard_html(metrics: Dict) -> str:
    cards = [
        ("Total Events", metrics["total_events"]),
        ("Rule Match Rate", _format_rate(metrics["rule_match_rate"])),
        ("Memory Reuse Rate", _format_rate(metrics["memory_match_rate"])),
        ("Documentation Coverage", _format_rate(metrics["documentation_found_rate"])),
        ("LLM Usage Rate", _format_rate(metrics["llm_usage_rate"])),
        ("Execution Success Rate", _format_rate(metrics["execution_success_rate"])),
        ("Promotion Rate", _format_rate(metrics["promotion_rate"])),
        ("Unresolved Rate", _format_rate(metrics["unresolved_rate"])),
    ]

    card_html = "\n".join(
        f"""
        <div class="card">
            <span>{label}</span>
            <strong>{value}</strong>
        </div>
        """
        for label, value in cards
    )

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Operations Engine Control Plane</title>
    <style>
        body {{
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            background: #0f172a;
            color: #e5e7eb;
        }}

        header {{
            padding: 32px;
            background: linear-gradient(135deg, #111827, #1e293b);
            border-bottom: 1px solid #334155;
        }}

        header h1 {{
            margin: 0;
            font-size: 32px;
        }}

        header p {{
            color: #94a3b8;
            margin-top: 8px;
            font-size: 16px;
        }}

        main {{
            padding: 32px;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }}

        .card {{
            background: #111827;
            border: 1px solid #334155;
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        }}

        .card span {{
            display: block;
            color: #94a3b8;
            font-size: 14px;
            margin-bottom: 8px;
        }}

        .card strong {{
            font-size: 30px;
            color: #38bdf8;
        }}

        .panels {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
        }}

        .panel {{
            background: #111827;
            border: 1px solid #334155;
            border-radius: 14px;
            padding: 20px;
        }}

        .panel h2 {{
            margin-top: 0;
            color: #f8fafc;
            font-size: 20px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th, td {{
            text-align: left;
            padding: 10px;
            border-bottom: 1px solid #334155;
        }}

        th {{
            color: #93c5fd;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        td {{
            color: #e5e7eb;
        }}

        .muted {{
            color: #94a3b8;
        }}

        .principle {{
            margin-top: 32px;
            padding: 24px;
            border-left: 4px solid #38bdf8;
            background: #020617;
            border-radius: 10px;
            color: #cbd5e1;
        }}

        footer {{
            padding: 20px 32px;
            color: #64748b;
            border-top: 1px solid #334155;
        }}
    </style>
</head>
<body>
    <header>
        <h1>AI Operations Engine Control Plane</h1>
        <p>Observability, governance and learning metrics for the AI Operations Engine.</p>
    </header>

    <main>
        <section class="grid">
            {card_html}
        </section>

        <section class="panels">
            {_build_table("Top Event Types", metrics["top_event_types"])}
            {_build_table("Top Rules", metrics["top_rules"])}
            {_build_table("Top Memories", metrics["top_memories"])}
            {_build_table("Documentation Gaps", metrics["documentation_gaps"])}
        </section>

        <section class="principle">
            <strong>Key principle:</strong>
            The system must not only automate operations — it must observe and evaluate itself.
        </section>
    </main>

    <footer>
        Generated from analytics trace events.
    </footer>
</body>
</html>
"""


def save_dashboard(metrics: Dict, output_path: str) -> None:
    html = build_dashboard_html(metrics)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")