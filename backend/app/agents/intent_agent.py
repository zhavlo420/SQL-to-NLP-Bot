def classify_intent(question: str) -> dict:
    q = question.lower()
    return {
        "operation": "aggregation" if any(x in q for x in ["revenue","sales","average","total","count"]) else "lookup",
        "needs_ranking": any(x in q for x in ["top","highest","lowest","best"]),
        "time_sensitive": any(x in q for x in ["today","month","quarter","year","last"])
    }
