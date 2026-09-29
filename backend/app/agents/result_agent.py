def analyze_result(question: str, result: dict) -> dict:
    rows = result.get("rows", [])
    if not rows:
        return {"summary": "The query returned no rows.", "chart": None}
    cols = result.get("columns", [])
    return {
        "summary": f"The query returned {len(rows)} row(s).",
        "chart": {
            "type": "bar" if len(rows) <= 20 and len(cols) >= 2 else "table",
            "x": cols[0] if cols else None,
            "y": cols[1] if len(cols) > 1 else None
        }
    }
