import json
from itertools import cycle
from pathlib import Path

VOCAB_PATH = Path(__file__).resolve().parent.parent / "data" / "vocabulary" / "vocabulary.json"

NOUN_TEMPLATES = [
    {
        "de": "Für die Höflinge bleibt {word_de} ein ständiges Thema.",
        "ru": "Для придворных «{translation_ru}» — постоянная тема.",
    },
    {
        "de": "Lears Herz wird schwer, wenn {word_de} zur Sprache kommt.",
        "ru": "Сердце Лира тяжелеет: «{translation_ru}» звучит слишком близко.",
    },
    {
        "de": "Im Thronsaal verstummen die Gespräche über {word_de} nie.",
        "ru": "В тронном зале постоянно звучит слово «{translation_ru}».",
    },
    {
        "de": "Der Narr spottet, sobald {word_de} erwähnt wird.",
        "ru": "Шут насмехается, едва кто-то произносит «{translation_ru}».",
    },
    {
        "de": "Cordelia merkt sich genau, wie {word_de} verteilt wird.",
        "ru": "Корделия внимательно следит, кому достанется «{translation_ru}».",
    },
    {
        "de": "Während des Sturms wirkt {word_de} noch bedrückender.",
        "ru": "Во время бури само «{translation_ru}» звучит ещё тяжелее.",
    },
]

VERB_TEMPLATES = [
    {
        "de": "Das {word_de_cap} fällt Lear unerwartet schwer.",
        "ru": "Лиру неожиданно тяжело {translation_ru}.",
    },
    {
        "de": "Cordelia zeigt, dass das {word_de_cap} auch ohne Stolz möglich ist.",
        "ru": "Корделия показывает, что {translation_ru} можно и без гордыни.",
    },
    {
        "de": "Im Sturm zeigt sich, wie wichtig das {word_de_cap} ist.",
        "ru": "Во время бури становится понятно, насколько важно {translation_ru}.",
    },
    {
        "de": "Der Narr spürt, wie das {word_de_cap} alle verändert.",
        "ru": "Шут чувствует, как умение {translation_ru} меняет всех.",
    },
]


def nominalize(verb: str) -> str:
    if not verb:
        return ""
    return verb[0].upper() + verb[1:]


def update_examples(path: Path) -> None:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    noun_cycle = cycle(NOUN_TEMPLATES)
    verb_cycle = cycle(VERB_TEMPLATES)

    for entry in data.get("vocabulary", []):
        part = entry.get("part_of_speech")
        if part == "существительное":
            template = next(noun_cycle)
            replacements = {
                "word_de": entry.get("german", ""),
                "translation_ru": entry.get("translation", ""),
            }
        elif part == "глагол":
            template = next(verb_cycle)
            replacements = {
                "word_de": entry.get("german", ""),
                "word_de_cap": nominalize(entry.get("german", "")),
                "translation_ru": entry.get("translation", ""),
            }
        else:
            template = {
                "de": "In Lears Reich klingt {word_de} nach Schicksal.",
                "ru": "В королевстве Лира «{translation_ru}» звучит как судьба.",
            }
            replacements = {
                "word_de": entry.get("german", ""),
                "translation_ru": entry.get("translation", ""),
            }

        entry["example_sentences"] = [
            {
                "de": template["de"].format(**replacements),
                "ru": template["ru"].format(**replacements),
            }
        ]

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    update_examples(VOCAB_PATH)
