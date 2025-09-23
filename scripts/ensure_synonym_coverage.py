"""Ensure that every vocabulary item has a synonym/antonym set.

The original data set ships with many journey phases where only a handful
of vocabulary entries include ``synonym_antonym_sets``.  The web
application expects one semantic field per vocabulary word.  This script
fills the gaps in a deterministic way while re-using as much information
from ``data/vocabulary/vocabulary.json`` as possible.

The workflow is as follows:

1. Load the global vocabulary catalogue to obtain part-of-speech tags,
   themes and translations for every German word that appears inside the
   character files.
2. For each missing vocabulary entry collect German synonyms from the
   thematic hints present in the catalogue.  Whenever the themes do not
   provide enough material, a curated set of fallback synonym/antonym
   pools keyed by semantic keywords is used.
3. Update the ``synonym_antonym_sets`` list inside the journey phase so
   that its order matches the order of the ``vocabulary`` section.  Any
   pre-existing entries are preserved.

The resulting data guarantees:

* Every vocabulary word has exactly one semantic field.
* Each field contains at least three German synonyms and two antonyms
  (also German).
* The generated text remains context aware thanks to the curated pools
  and narration templates.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence


ROOT = Path(__file__).resolve().parents[1]
CHARACTERS_DIR = ROOT / "data" / "characters"
VOCABULARY_PATH = ROOT / "data" / "vocabulary" / "vocabulary.json"


@dataclass(frozen=True)
class LexicalEntry:
    word: str
    translation: str


def load_vocabulary_lookup() -> Dict[str, dict]:
    with VOCABULARY_PATH.open("r", encoding="utf-8") as fh:
        raw = json.load(fh)
    return {item["german"]: item for item in raw.get("vocabulary", [])}


VOCAB = load_vocabulary_lookup()
GERMAN_INDEX = {word.lower(): meta for word, meta in VOCAB.items()}


def part_of_speech_tag(word: str) -> str:
    meta = VOCAB[word]
    raw = meta.get("part_of_speech", "").lower()
    if "глагол" in raw:
        return "verb"
    if "прилаг" in raw:
        return "adjective"
    if "нареч" in raw:
        return "adverb"
    return "noun"


def lookup_translation(german_word: str) -> Optional[str]:
    meta = GERMAN_INDEX.get(german_word.lower())
    if meta:
        return meta.get("translation")
    return None


def from_pairs(pairs: Sequence[tuple[str, str]]) -> List[LexicalEntry]:
    return [LexicalEntry(word=w, translation=t) for w, t in pairs]


# ---------------------------------------------------------------------------
# Fallback pools grouped by semantic keywords.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SemanticPool:
    keywords: Sequence[str]
    synonyms: Dict[str, List[LexicalEntry]]
    antonyms: Dict[str, List[LexicalEntry]]
    narration: str

    def matches(self, german: str, translation: str) -> bool:
        g = german.lower()
        t = translation.lower()
        return any(key in g or key in t for key in self.keywords)

    def pick_synonyms(self, pos: str) -> List[LexicalEntry]:
        return self.synonyms.get(pos, self.synonyms.get("generic", []))

    def pick_antonyms(self, pos: str) -> List[LexicalEntry]:
        return self.antonyms.get(pos, self.antonyms.get("generic", []))


SEMANTIC_POOLS: List[SemanticPool] = [
    SemanticPool(
        keywords=(
            "трон",
            "корон",
            "королев",
            "власт",
            "герц",
            "граф",
            "монарх",
            "король",
            "reich",
            "herrsch",
            "adel",
        ),
        synonyms={
            "noun": from_pairs(
                [
                    ("die Herrschaft", "власть"),
                    ("das Reich", "королевство"),
                    ("die Königswürde", "королевское достоинство"),
                    ("das Zepter", "скипетр"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("regieren", "править"),
                    ("gebieten", "повелевать"),
                    ("thronen", "восседать"),
                    ("krönen", "короновать"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("majestätisch", "величественный"),
                    ("herrschaftlich", "царственный"),
                    ("glanzvoll", "сверкающий"),
                    ("prachtvoll", "роскошный"),
                ]
            ),
            "adverb": from_pairs(
                [
                    ("majestätisch", "величественно"),
                    ("erhaben", "возвышенно"),
                    ("glorreich", "славно"),
                ]
            ),
        },
        antonyms={
            "generic": from_pairs(
                [
                    ("die Ohnmacht", "бессилие"),
                    ("der Sturz", "падение"),
                    ("die Verbannung", "изгнание"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("gehorchen", "подчиняться"),
                    ("folgen", "следовать"),
                    ("entsagen", "отказываться"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("schlicht", "простой"),
                    ("armselig", "убогий"),
                    ("gewöhnlich", "обычный"),
                ]
            ),
            "adverb": from_pairs(
                [
                    ("bescheiden", "скромно"),
                    ("niedrig", "низко"),
                ]
            ),
        },
        narration="От величия короны к пониманию её утраты.",
    ),
    SemanticPool(
        keywords=(
            "церем",
            "торжествен",
            "праздн",
            "ритуал",
            "verkünd",
            "ansage",
            "zeremon",
            "feier",
        ),
        synonyms={
            "generic": from_pairs(
                [
                    ("die Feier", "праздник"),
                    ("der Ritus", "ритуал"),
                    ("die Verkündung", "объявление"),
                    ("die Zeremonie", "церемония"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("verkünden", "провозглашать"),
                    ("ausrufen", "восклицать"),
                    ("zelebrieren", "отмечать"),
                    ("feiern", "праздновать"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("feierlich", "торжественный"),
                    ("glänzend", "сияющий"),
                    ("erhebend", "возвышенный"),
                ]
            ),
            "adverb": from_pairs(
                [
                    ("feierlich", "торжественно"),
                    ("öffentlich", "публично"),
                    ("laut", "громко"),
                ]
            ),
        },
        antonyms={
            "generic": from_pairs(
                [
                    ("der Alltag", "повседневность"),
                    ("das Schweigen", "молчание"),
                    ("die Spontaneität", "спонтанность"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("verschweigen", "утаивать"),
                    ("verheimlichen", "скрывать"),
                    ("unterlassen", "пропускать"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("alltäglich", "повседневный"),
                    ("still", "тихий"),
                    ("unscheinbar", "невзрачный"),
                ]
            ),
            "adverb": from_pairs(
                [
                    ("heimlich", "тайно"),
                    ("leise", "тихо"),
                ]
            ),
        },
        narration="От громких объявлений к тишине скрытых тайн.",
    ),
    SemanticPool(
        keywords=(
            "предател",
            "измен",
            "обман",
            "ложь",
            "ковар",
            "интриг",
            "хитр",
            "mask",
            "täusch",
            "lüg",
            "falsch",
            "list",
        ),
        synonyms={
            "generic": from_pairs(
                [
                    ("der Betrug", "обман"),
                    ("die Intrige", "интрига"),
                    ("die Hinterlist", "коварство"),
                    ("die Falschheit", "фальшь"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("täuschen", "обманывать"),
                    ("betrügen", "жульничать"),
                    ("hintergehen", "подводить"),
                    ("manipulieren", "манипулировать"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("falsch", "лживый"),
                    ("verschlagen", "хитрый"),
                    ("verlogen", "лживый"),
                ]
            ),
            "adverb": from_pairs(
                [
                    ("heimlich", "тайно"),
                    ("listig", "хитро"),
                    ("hinterhältig", "коварно"),
                ]
            ),
        },
        antonyms={
            "generic": from_pairs(
                [
                    ("die Ehrlichkeit", "честность"),
                    ("die Offenheit", "открытость"),
                    ("die Loyalität", "лояльность"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("offenbaren", "раскрывать"),
                    ("gestehen", "признавать"),
                    ("vertrauen", "доверять"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("ehrlich", "честный"),
                    ("aufrichtig", "искренний"),
                    ("loyal", "лояльный"),
                ]
            ),
            "adverb": from_pairs(
                [
                    ("offen", "открыто"),
                    ("ehrlich", "честно"),
                ]
            ),
        },
        narration="От теней интриг к свету честности.",
    ),
    SemanticPool(
        keywords=(
            "гнев",
            "ярост",
            "злоб",
            "прокл",
            "fluch",
            "zorn",
            "wut",
            "kränk",
            "оскорб",
        ),
        synonyms={
            "generic": from_pairs(
                [
                    ("der Zorn", "гнев"),
                    ("die Wut", "ярость"),
                    ("der Fluch", "проклятие"),
                    ("die Kränkung", "обида"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("fluchen", "проклинать"),
                    ("schimpfen", "бранить"),
                    ("toben", "бушевать"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("zornig", "гневный"),
                    ("wütend", "яростный"),
                    ("erbost", "разъярённый"),
                ]
            ),
            "adverb": from_pairs(
                [
                    ("wütend", "яростно"),
                    ("erbittert", "озлобленно"),
                ]
            ),
        },
        antonyms={
            "generic": from_pairs(
                [
                    ("die Ruhe", "спокойствие"),
                    ("die Versöhnung", "примирение"),
                    ("die Vergebung", "прощение"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("vergeben", "прощать"),
                    ("beschwichtigen", "успокаивать"),
                    ("segnen", "благословлять"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("gelassen", "невозмутимый"),
                    ("friedlich", "мирный"),
                    ("versöhnlich", "примирительный"),
                ]
            ),
            "adverb": from_pairs(
                [
                    ("ruhig", "спокойно"),
                    ("mild", "кротко"),
                ]
            ),
        },
        narration="От вспышек ярости к тихому примирению.",
    ),
    SemanticPool(
        keywords=(
            "страдан",
            "боль",
            "рана",
            "тоска",
            "скорб",
            "страх",
            "печал",
            "leiden",
            "schmerz",
            "traur",
            "weinen",
            "blut",
            "wunde",
        ),
        synonyms={
            "generic": from_pairs(
                [
                    ("das Leid", "страдание"),
                    ("der Schmerz", "боль"),
                    ("die Qual", "мука"),
                    ("die Trauer", "скорбь"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("leiden", "страдать"),
                    ("bluten", "кровоточить"),
                    ("klagen", "жаловаться"),
                    ("weinen", "плакать"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("leidend", "страдальческий"),
                    ("verzweifelt", "отчаянный"),
                    ("traurig", "печальный"),
                ]
            ),
            "adverb": from_pairs(
                [
                    ("schmerzlich", "болезненно"),
                    ("klagend", "жалобно"),
                ]
            ),
        },
        antonyms={
            "generic": from_pairs(
                [
                    ("die Freude", "радость"),
                    ("das Glück", "счастье"),
                    ("die Heilung", "исцеление"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("heilen", "исцелять"),
                    ("lindern", "облегчать"),
                    ("trösten", "утешать"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("heil", "целый"),
                    ("fröhlich", "весёлый"),
                    ("getröstet", "утешенный"),
                ]
            ),
        },
        narration="От глубокой боли к надежде на исцеление.",
    ),
    SemanticPool(
        keywords=(
            "бур",
            "шторм",
            "гроза",
            "молни",
            "ветер",
            "стих",
            "sturm",
            "gewitter",
            "donner",
            "blitz",
        ),
        synonyms={
            "generic": from_pairs(
                [
                    ("der Sturm", "буря"),
                    ("das Unwetter", "непогода"),
                    ("der Orkan", "ураган"),
                    ("das Gewitter", "гроза"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("toben", "бушевать"),
                    ("brausen", "шуметь"),
                    ("peitschen", "хлестать"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("stürmisch", "бурный"),
                    ("tosend", "ревущий"),
                    ("wild", "яростный"),
                ]
            ),
            "adverb": from_pairs(
                [
                    ("stürmisch", "бурно"),
                    ("heftig", "яростно"),
                ]
            ),
        },
        antonyms={
            "generic": from_pairs(
                [
                    ("die Ruhe", "покой"),
                    ("die Stille", "тишина"),
                    ("die Windstille", "штиль"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("beruhigen", "успокаивать"),
                    ("abflauen", "утихать"),
                    ("ruhen", "покоиться"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("ruhig", "спокойный"),
                    ("still", "тихий"),
                    ("sanft", "мягкий"),
                ]
            ),
        },
        narration="От ярости стихии к тишине штиля.",
    ),
    SemanticPool(
        keywords=(
            "безум",
            "сумас",
            "помеш",
            "irr",
            "wahnsinn",
            "verrückt",
            "geist",
            "умоп",
            "ошиб",
            "irrung",
        ),
        synonyms={
            "generic": from_pairs(
                [
                    ("der Wahnsinn", "безумие"),
                    ("die Raserei", "безумство"),
                    ("der Irrsinn", "помешательство"),
                    ("die Verwirrung", "смятение"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("toben", "бесноваться"),
                    ("fantasieren", "бредить"),
                    ("irren", "ошибаться"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("wahnsinnig", "безумный"),
                    ("irr", "помешанный"),
                    ("verwirrt", "смущённый"),
                ]
            ),
            "adverb": from_pairs(
                [
                    ("wahnsinnig", "безумно"),
                    ("irr", "безрассудно"),
                ]
            ),
        },
        antonyms={
            "generic": from_pairs(
                [
                    ("die Vernunft", "разум"),
                    ("die Klarheit", "ясность"),
                    ("die Besonnenheit", "рассудительность"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("ordnen", "упорядочивать"),
                    ("beruhigen", "успокаивать"),
                    ("klären", "прояснять"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("klar", "ясный"),
                    ("vernünftig", "разумный"),
                    ("besonnen", "рассудительный"),
                ]
            ),
        },
        narration="От вихря безумия к свету рассудка.",
    ),
    SemanticPool(
        keywords=(
            "бедн",
            "нищ",
            "убог",
            "гол",
            "elend",
            "arm",
            "kälte",
            "frieren",
            "bettler",
        ),
        synonyms={
            "generic": from_pairs(
                [
                    ("die Armut", "бедность"),
                    ("die Bedürftigkeit", "нужда"),
                    ("die Not", "нужда"),
                    ("die Entbehrung", "лишение"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("frieren", "мёрзнуть"),
                    ("darben", "голодать"),
                    ("betteln", "просить подаяние"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("arm", "бедный"),
                    ("elend", "жалкий"),
                    ("mittellos", "без средств"),
                ]
            ),
            "adverb": from_pairs(
                [
                    ("elend", "жалко"),
                    ("armselig", "убого"),
                ]
            ),
        },
        antonyms={
            "generic": from_pairs(
                [
                    ("der Reichtum", "богатство"),
                    ("der Wohlstand", "процветание"),
                    ("die Fülle", "достаток"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("reich", "богатый"),
                    ("wohlhabend", "состоятельный"),
                    ("überflussig", "изобильный"),
                ]
            ),
        },
        narration="От холода нищеты к мечте о достатке.",
    ),
    SemanticPool(
        keywords=(
            "прощ",
            "милос",
            "раская",
            "искуп",
            "утеш",
            "благод",
            "gnade",
            "erlös",
            "vergeb",
            "tröst",
        ),
        synonyms={
            "generic": from_pairs(
                [
                    ("die Vergebung", "прощение"),
                    ("die Gnade", "милость"),
                    ("die Erlösung", "искупление"),
                    ("das Mitgefühl", "сострадание"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("vergeben", "прощать"),
                    ("verzeihen", "извинять"),
                    ("erlösen", "освобождать"),
                    ("trösten", "утешать"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("barmherzig", "милосердный"),
                    ("sanft", "нежный"),
                    ("gnädig", "милостивый"),
                ]
            ),
        },
        antonyms={
            "generic": from_pairs(
                [
                    ("die Rache", "месть"),
                    ("die Strafe", "наказание"),
                    ("die Härte", "жестокость"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("rächen", "мстить"),
                    ("bestrafen", "наказывать"),
                    ("verurteilen", "осудить"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("unbarmherzig", "беспощадный"),
                    ("hart", "жёсткий"),
                    ("vergeltend", "карательный"),
                ]
            ),
        },
        narration="От тяжёлого покаяния к свету милосердия.",
    ),
    SemanticPool(
        keywords=(
            "битв",
            "бой",
            "дуэль",
            "армия",
            "сраж",
            "меч",
            "щит",
            "kampf",
            "krieg",
            "schlacht",
        ),
        synonyms={
            "generic": from_pairs(
                [
                    ("der Kampf", "битва"),
                    ("die Schlacht", "сражение"),
                    ("das Gefecht", "бой"),
                    ("die Auseinandersetzung", "столкновение"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("kämpfen", "сражаться"),
                    ("streiten", "бороться"),
                    ("angreifen", "атаковать"),
                    ("verteidigen", "защищать"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("tapfer", "храбрый"),
                    ("mutig", "смелый"),
                    ("kriegerisch", "воинственный"),
                ]
            ),
        },
        antonyms={
            "generic": from_pairs(
                [
                    ("der Frieden", "мир"),
                    ("die Kapitulation", "капитуляция"),
                    ("die Ruhe", "спокойствие"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("nachgeben", "уступать"),
                    ("fliehen", "бежать"),
                    ("sich ergeben", "сдаваться"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("feige", "трусливый"),
                    ("friedlich", "мирный"),
                    ("passiv", "пассивный"),
                ]
            ),
        },
        narration="От звона мечей к тишине мира.",
    ),
    SemanticPool(
        keywords=(
            "судьб",
            "рок",
            "пророч",
            "знам",
            "ом",
            "предчув",
            "ahnung",
            "prophe",
            "schicksal",
            "omen",
            "rätsel",
            "tückisch",
        ),
        synonyms={
            "generic": from_pairs(
                [
                    ("das Schicksal", "судьба"),
                    ("die Prophezeiung", "пророчество"),
                    ("die Vorahnung", "предчувствие"),
                    ("das Omen", "знамение"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("ahnen", "предчувствовать"),
                    ("vorhersagen", "предсказывать"),
                    ("deuten", "толковать"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("rätselhaft", "загадочный"),
                    ("prophetisch", "пророческий"),
                    ("unheilvoll", "зловещий"),
                ]
            ),
        },
        antonyms={
            "generic": from_pairs(
                [
                    ("der Zufall", "случайность"),
                    ("die Freiheit", "свобода"),
                    ("die Klarheit", "ясность"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("ignorieren", "игнорировать"),
                    ("zweifeln", "сомневаться"),
                    ("vergessen", "забывать"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("klar", "ясный"),
                    ("offensichtlich", "очевидный"),
                    ("geerdet", "приземлённый"),
                ]
            ),
        },
        narration="От загадок судьбы к ясности выбора.",
    ),
    SemanticPool(
        keywords=(
            "музык",
            "песн",
            "мелод",
            "рифм",
            "klingen",
            "lied",
            "reim",
            "melodie",
            "summen",
            "singen",
        ),
        synonyms={
            "generic": from_pairs(
                [
                    ("das Lied", "песня"),
                    ("die Melodie", "мелодия"),
                    ("der Gesang", "пение"),
                    ("der Klang", "звучание"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("singen", "петь"),
                    ("summen", "напевать"),
                    ("klingen", "звучать"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("melodisch", "мелодичный"),
                    ("rhythmisch", "ритмичный"),
                    ("klangvoll", "звучный"),
                ]
            ),
        },
        antonyms={
            "generic": from_pairs(
                [
                    ("die Stille", "тишина"),
                    ("das Schweigen", "молчание"),
                    ("die Dissonanz", "диссонанс"),
                ]
            ),
            "verb": from_pairs(
                [
                    ("verstummen", "замолкать"),
                    ("schweigen", "молчать"),
                    ("verstummen", "затихать"),
                ]
            ),
            "adjective": from_pairs(
                [
                    ("stumm", "немой"),
                    ("tonlos", "беззвучный"),
                    ("rau", "грубый"),
                ]
            ),
        },
        narration="От звучащей песни к тишине задумчивости.",
    ),
]

FALLBACK_POOL = SemanticPool(
    keywords=("",),
    synonyms={
        "noun": from_pairs(
            [
                ("der Gedanke", "мысль"),
                ("das Bild", "образ"),
                ("das Motiv", "мотив"),
                ("der Begriff", "понятие"),
            ]
        ),
        "verb": from_pairs(
            [
                ("handeln", "действовать"),
                ("gestalten", "создавать"),
                ("bewegen", "двигать"),
                ("wirken", "влиять"),
            ]
        ),
        "adjective": from_pairs(
            [
                ("bedeutend", "значительный"),
                ("prägend", "формирующий"),
                ("markant", "выразительный"),
            ]
        ),
        "adverb": from_pairs(
            [
                ("deutlich", "отчётливо"),
                ("klar", "ясно"),
                ("bestimmt", "определённо"),
            ]
        ),
    },
    antonyms={
        "generic": from_pairs(
            [
                ("die Leere", "пустота"),
                ("das Vergessen", "забвение"),
                ("die Gleichgültigkeit", "равнодушие"),
            ]
        ),
        "verb": from_pairs(
            [
                ("unterlassen", "упускать"),
                ("verharren", "застаиваться"),
                ("erstarren", "замирать"),
            ]
        ),
        "adjective": from_pairs(
            [
                ("bedeutungslos", "незначительный"),
                ("farblos", "бесцветный"),
                ("passiv", "пассивный"),
            ]
        ),
    },
    narration="От любого понятия к его забвению.",
)


def find_semantic_pool(german: str, translation: str) -> SemanticPool:
    for pool in SEMANTIC_POOLS:
        if pool.matches(german, translation):
            return pool
    return FALLBACK_POOL


def collect_theme_synonyms(word: str) -> List[LexicalEntry]:
    themes = VOCAB[word].get("themes", [])
    entries: List[LexicalEntry] = []
    for theme in themes:
        candidate = GERMAN_INDEX.get(theme.lower())
        if not candidate:
            continue
        german_word = candidate["german"]
        if german_word == word:
            continue
        translation = candidate.get("translation", "")
        entries.append(LexicalEntry(word=german_word, translation=translation))
        if len(entries) >= 3:
            break
    return entries


def ensure_capacity(entries: List[LexicalEntry], desired: int, pool: List[LexicalEntry], *, forbid: str) -> List[LexicalEntry]:
    used_words = {e.word for e in entries}
    if forbid:
        used_words.add(forbid)
    for candidate in pool:
        if candidate.word in used_words:
            continue
        entries.append(candidate)
        used_words.add(candidate.word)
        if len(entries) >= desired:
            break
    return entries[:desired]


def build_synonym_set(vocab_entry: dict, narration: str) -> dict:
    german = vocab_entry["german"]
    translation = vocab_entry.get("russian") or vocab_entry.get("translation", "")
    pos = part_of_speech_tag(german)
    pool = find_semantic_pool(german, translation)

    synonyms = collect_theme_synonyms(german)
    synonyms = ensure_capacity(synonyms, 3, pool.pick_synonyms(pos), forbid=german)
    if len(synonyms) < 3:
        synonyms = ensure_capacity(synonyms, 3, FALLBACK_POOL.pick_synonyms(pos), forbid=german)

    antonyms: List[LexicalEntry] = []
    antonyms = ensure_capacity(antonyms, 2, pool.pick_antonyms(pos), forbid="")
    if len(antonyms) < 2:
        antonyms = ensure_capacity(antonyms, 2, FALLBACK_POOL.pick_antonyms(pos), forbid="")

    return {
        "id": f"{vocab_entry.get('phase_id', 'phase')}_{german.replace(' ', '_').replace('/', '_').lower()}",
        "title": f"Семантическое поле: {translation}",
        "target": {
            "word": german,
            "translation": translation,
            "hint": vocab_entry.get("russian_hint", ""),
        },
        "synonyms": [
            {"word": entry.word, "translation": entry.translation} for entry in synonyms
        ],
        "antonyms": [
            {"word": entry.word, "translation": entry.translation} for entry in antonyms
        ],
        "narration": narration,
    }


def ensure_phase_sets(phase: dict) -> bool:
    vocabulary = phase.get("vocabulary", [])
    existing = phase.get("synonym_antonym_sets", [])
    existing_by_word = {
        entry.get("target", {}).get("word"): entry for entry in existing if entry.get("target")
    }

    updated_sets: List[dict] = []
    changed = False
    for vocab in vocabulary:
        german = vocab["german"]
        if german in existing_by_word:
            updated_sets.append(existing_by_word[german])
            continue

        narration = find_semantic_pool(german, vocab.get("russian", "")).narration
        enriched_vocab = {**vocab, "phase_id": phase.get("id", "phase")}
        new_set = build_synonym_set(enriched_vocab, narration)
        updated_sets.append(new_set)
        changed = True

    if changed or len(existing_by_word) != len(updated_sets):
        phase["synonym_antonym_sets"] = updated_sets
    return changed


def process_character(path: Path) -> bool:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    changed = False
    for phase in data.get("journey_phases", []):
        if ensure_phase_sets(phase):
            changed = True

    if changed:
        with path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

    return changed


def main() -> None:
    changed_files: List[str] = []
    for json_file in sorted(CHARACTERS_DIR.glob("*.json")):
        if process_character(json_file):
            changed_files.append(json_file.name)

    print("[SYNONYM COVERAGE REPORT]")
    if changed_files:
        print(f"Updated files ({len(changed_files)}): {', '.join(changed_files)}")
    else:
        print("All character files already have complete coverage.")


if __name__ == "__main__":
    main()
