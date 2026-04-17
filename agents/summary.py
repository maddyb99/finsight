import json
import os

SYSTEM_PROMPT = (
    "You are a financial analyst. Given structured anomaly-detection and "
    "driver-analysis findings, write a concise executive summary. "
    "Rules: use ONLY the numbers provided; do not invent figures. "
    "Explain what was unusual and the main drivers, in plain business English. "
    "Keep it to 3-5 short paragraphs. No preamble."
)


def _format_findings(findings: dict) -> str:
    return json.dumps(findings, indent=2)


def generate_summary(findings: dict) -> str:

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return _fallback_summary(findings)

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents="Findings:\n" + _format_findings(findings),
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=800,
            ),
        )
        return response.text.strip()
    except Exception as exc:  # noqa: BLE001 - demo resilience
        return _fallback_summary(findings, error=str(exc))


def _fallback_summary(findings: dict, error: str | None = None) -> str:
    lines = []
    if error:
        lines.append(f"[LLM unavailable: {error}. Templated summary below.]")
    n = findings.get("n_anomalies", 0)
    lines.append(
        f"Analysis flagged {n} anomalous period(s) out of {findings.get('n_periods', 0)} using {findings.get('method', 'anomaly detection')}."
    )
    for a in findings.get("anomalies", []):
        drv = a.get("drivers", [])
        top = drv[0]["category"] if drv else "n/a"
        lines.append(
            f"- {a['period']}: value {a['value']} ({a['pct_change']:+.1f}% vs prior). Primary driver: {top}."
        )
    return "\n".join(lines)
