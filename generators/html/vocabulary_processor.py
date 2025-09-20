"""Vocabulary enrichment helpers for journey pages."""
from __future__ import annotations
import json, re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from utils.text_processing import collapse_whitespace

_VARIANT_OVERRIDES = {
    "трон": "троне", "церемония": "церемонию", "гнев": "гнев",
    "проклятие": "проклятием", "нищета": "нищету", "хижина": "хижине",
    "правда": "правду", "конец": "концом", "слеза": "слезы",
    "нужда": "нужде", "вечный": "вечна",
}

def _ensure_list(value: Any) -> List[str]:
    if not value:
        return []
    if isinstance(value, str):
        return [value.strip()]
    if isinstance(value, (list, tuple)):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]

class VocabularyProcessor:
    """Load shared vocabulary and enrich character data."""

    def __init__(self, data_dir: Path) -> None:
        self.vocabulary_path = Path(data_dir) / "vocabulary" / "vocabulary.json"
        self._cache: Optional[Dict[str, Dict[str, Any]]] = None

    def load_cache(self) -> Dict[str, Dict[str, Any]]:
        if self._cache is None:
            data = []
            if self.vocabulary_path.exists():
                with self.vocabulary_path.open("r", encoding="utf-8") as handle:
                    data = json.load(handle).get("vocabulary", [])
            self._cache = {
                collapse_whitespace(entry.get("german", "")).lower(): entry
                for entry in data
                if collapse_whitespace(entry.get("german", ""))
            }
        return self._cache

    def enrich_character(self, character: Dict[str, Any]) -> None:
        vocab_index = self.load_cache()
        if not vocab_index:
            return
        for phase in character.get("journey_phases", []):
            for word in phase.get("vocabulary", []):
                entry = vocab_index.get(collapse_whitespace(word.get("german", "")).lower())
                if entry:
                    self._apply_defaults(word, entry)

    @staticmethod
    def _apply_defaults(word: Dict[str, Any], entry: Dict[str, Any]) -> None:
        for key, source_key in (("wordFamily", "word_family"), ("synonyms", "synonyms"), ("collocations", "collocations")):
            if not word.get(key) and (values := _ensure_list(entry.get(source_key))):
                word[key] = values
        if not word.get("visual_hint") and entry.get("visual_hint"):
            word["visual_hint"] = entry["visual_hint"]
        if not word.get("themes") and (themes := _ensure_list(entry.get("themes"))):
            word["themes"] = themes

    def relations_metadata(self, journey_phases: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, bool]]:
        metadata: Dict[str, Dict[str, bool]] = {}
        for index, phase in enumerate(journey_phases):
            words = phase.get("vocabulary", [])
            has_family = any(_ensure_list(item.get("wordFamily")) for item in words)
            has_synonyms = any(_ensure_list(item.get("synonyms")) for item in words)
            has_collocations = any(_ensure_list(item.get("collocations")) for item in words)
            metadata[phase.get("id", f"phase-{index}")] = {
                "has_word_families": has_family,
                "has_synonyms": has_synonyms,
                "has_collocations": has_collocations,
                "has_relations": has_family or has_synonyms or has_collocations,
            }
        return metadata

    def words_dictionary(self, phase: Dict[str, Any], scene: Dict[str, Any]) -> Dict[str, str]:
        words: Dict[str, str] = {}
        for vocab in phase.get("vocabulary", []):
            russian = vocab.get("russian", "")
            base = self._format_german(vocab.get("german", ""))
            if russian:
                words[russian] = base
                variant = _VARIANT_OVERRIDES.get(russian)
                if variant:
                    words[variant] = base
        for german, russian in re.findall(r'<b>([^(]+)\s*\(([^)]+)\)</b>', scene.get("narrative", "")):
            hint = collapse_whitespace(russian)
            if hint and hint not in words:
                words[hint] = collapse_whitespace(german)
        return words

    @staticmethod
    def _format_german(german: str) -> str:
        if german.startswith(("der ", "die ", "das ")):
            article, rest = german.split(" ", 1)
            return f"{article} {rest.upper()}"
        return german.upper()
