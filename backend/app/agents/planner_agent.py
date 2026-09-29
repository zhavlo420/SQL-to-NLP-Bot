def make_plan(
    question: str,
    intent: dict,
    schema: list[dict],
    glossary: list[dict] | None = None,
) -> list[str]:
    plan = [
        "Identify required tables and columns.",
        "Resolve relationships through keys.",
        "Translate filters, aggregation, grouping, sorting and limits.",
        "Generate dialect-specific SQL.",
        "Validate semantics, security and result shape."
    ]
    if glossary:
        definitions = "; ".join(
            f"{entry['term']}: {entry['definition']}" for entry in glossary
        )
        plan.append(f"Apply retrieved business definitions: {definitions}")
    return plan
