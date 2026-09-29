import json
import re
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def load_business_glossary() -> list[dict]:
    path = Path(__file__).resolve().parent.parent / "data" / "business_glossary.json"
    with path.open(encoding="utf-8") as glossary_file:
        return json.load(glossary_file)


def _normalize(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def _tokens(text: str) -> set[str]:
    return set(_normalize(text).split())


def retrieve_glossary(question: str, max_results: int = 5) -> list[dict]:
    normalized_question = f" {_normalize(question)} "
    question_tokens = _tokens(question)
    matches = []

    for entry in load_business_glossary():
        phrases = [entry["term"], *entry.get("aliases", [])]
        normalized_phrases = [_normalize(phrase) for phrase in phrases]
        phrase_matches = sum(
            f" {phrase} " in normalized_question
            for phrase in normalized_phrases
            if phrase
        )
        entry_tokens = set().union(*(_tokens(phrase) for phrase in phrases))
        score = phrase_matches * 4 + len(question_tokens & entry_tokens)
        if score:
            matches.append((score, entry))

    matches.sort(key=lambda match: (-match[0], match[1]["term"]))
    return [entry for _, entry in matches[:max_results]]


def canonicalize_question(question: str, glossary: list[dict]) -> str:
    aliases = [
        (alias, entry["term"])
        for entry in glossary
        for alias in entry.get("aliases", [])
    ]
    aliases.sort(key=lambda item: len(item[0]), reverse=True)

    canonical = question
    for alias, term in aliases:
        pattern = re.compile(rf"(?<!\w){re.escape(alias)}(?!\w)", re.IGNORECASE)
        canonical = pattern.sub(term, canonical)
    return canonical