#!/usr/bin/env python3
"""Enrich vocabulary.json with word family, synonyms and collocations."""

import json
import re
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1] / 'data'
VOCAB_PATH = BASE_DIR / 'vocabulary' / 'vocabulary.json'
CHAR_DIR = BASE_DIR / 'characters'

SEPARABLE_PREFIXES = [
    'ab', 'an', 'auf', 'aus', 'bei', 'dar', 'ein', 'fest', 'her', 'hin', 'mit',
    'nach', 'vor', 'weg', 'wieder', 'zu', 'zurück', 'zusammen', 'über'
]
INSEPARABLE_PREFIXES = ['be', 'ge', 'er', 'ver', 'zer', 'ent', 'emp', 'miss', 'hinter']


def load_data():
    with VOCAB_PATH.open('r', encoding='utf-8') as fp:
        vocab = json.load(fp)
    characters = []
    for path in CHAR_DIR.glob('*.json'):
        characters.append(json.loads(path.read_text(encoding='utf-8')))
    return vocab, characters


def ensure_usage(storage, german):
    if german not in storage:
        storage[german] = {
            'translations': set(),
            'transcriptions': set(),
            'part_of_speech': None,
            'gender': None,
            'examples': [],  # list of (de, ru)
            'characters': set(),
            'keywords': set(),
            'levels': set(),
            'themes': set(),
        }
    return storage[german]


def tokenize_translation(text):
    if not text:
        return []
    tokens = re.split(r'[\s,/;•\u2014\u2013]+', text)
    cleaned = []
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        token = token.strip('"«»')
        if token:
            cleaned.append(token)
    return cleaned


def detect_part_of_speech(word, usage):
    part = usage.get('part_of_speech')
    if part:
        return part
    translations = usage.get('translations') or set()
    translation = next(iter(translations), '')
    if word.startswith(('der ', 'die ', 'das ', 'dem ', 'den ')):
        return 'существительное'
    if word.startswith('sich '):
        return 'глагол'
    if translation:
        low = translation.lower()
        if any(low.endswith(suffix) for suffix in ('ть', 'ться', 'сти')):
            return 'глагол'
        if any(low.endswith(suffix) for suffix in ('ый', 'ий', 'ой', 'ая', 'ое', 'ее', 'чивый', 'тельный', 'ливый')):
            return 'прилагательное'
        if any(low.endswith(suffix) for suffix in ('ие', 'ия', 'ость', 'ство', 'ца', 'ок', 'ик', 'ец', 'ка', 'ль', 'ель', 'ие')):
            return 'существительное'
    if word and word[0].isupper():
        return 'существительное'
    if word.endswith(('en', 'ern', 'eln')):
        return 'глагол'
    if word.endswith(('ig', 'lich', 'isch', 'sam', 'los', 'bar', 'haft', 'end')):
        return 'прилагательное'
    return 'глагол'


def split_reflexive(word):
    if word.startswith('sich '):
        return 'sich', word[5:]
    return None, word


def stem_verb(base):
    if base.endswith('eln'):
        return base[:-3] + 'el'
    if base.endswith('ern'):
        return base[:-1]
    if base.endswith('en'):
        return base[:-2]
    if base.endswith('n'):
        return base[:-1]
    return base


def conjugate_ich(word):
    reflexive, base = split_reflexive(word)
    prefix = None
    remainder = base
    for pref in SEPARABLE_PREFIXES:
        if base.startswith(pref) and len(base) > len(pref) + 1:
            prefix = pref
            remainder = base[len(pref):]
            break
    stem = stem_verb(remainder)
    form = stem + 'e'
    if prefix:
        if reflexive:
            return f"ich {form} mich {prefix}"
        return f"ich {form} {prefix}"
    if reflexive:
        return f"ich {form} mich"
    return f"ich {form}"


def guess_participle(word):
    reflexive, base = split_reflexive(word)
    participle = base
    for pref in SEPARABLE_PREFIXES:
        if base.startswith(pref) and len(base) > len(pref) + 2:
            stem = base[len(pref):]
            core = stem_verb(stem)
            participle = f"{pref}ge{core}t"
            break
    else:
        for pref in INSEPARABLE_PREFIXES:
            if base.startswith(pref) and len(base) > len(pref) + 2:
                stem = base[len(pref):]
                core = stem_verb(stem)
                participle = f"{pref}{core}t"
                break
        else:
            if base.endswith('ieren'):
                participle = base[:-3] + 'rt'
            else:
                core = stem_verb(base)
                participle = f"ge{core}t"
    if reflexive:
        return f"hat sich {participle}"
    return f"hat {participle}"


def guess_plural(word, gender):
    if word.startswith(('der ', 'die ', 'das ')):
        base = word.split(' ', 1)[1]
    else:
        base = word
    lower = base.lower()
    if lower.endswith(('e', 'el', 'er', 'en')):
        plural = base
    elif lower.endswith('in'):
        plural = base + 'nen'
    elif lower.endswith(('ung', 'heit', 'keit')):
        plural = base + 'en'
    elif lower.endswith(('t', 's', 'ß', 'x', 'z', 'sch')):
        plural = base + 'e'
    elif lower.endswith('o'):
        plural = base + 's'
    elif lower.endswith('a'):
        plural = base + 'en'
    else:
        plural = base + 'e'
    return f"die {plural}"


def comparative_form(word):
    lower = word.lower()
    if lower.endswith('el'):
        return word[:-2] + 'ler'
    if lower.endswith('er'):
        return word[:-2] + 'rer'
    if lower.endswith('e'):
        return word + 'r'
    return word + 'er'


def superlative_form(word):
    lower = word.lower()
    ending = 'sten'
    if lower.endswith(('d', 't', 's', 'ß', 'x', 'z', 'sch')):
        ending = 'esten'
    return f"am {word}{ending}"


def unique_strings(items):
    seen = set()
    result = []
    for item in items:
        if not item:
            continue
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def unique_examples(examples):
    seen = set()
    result = []
    for de, ru in examples:
        key = (de or '', ru or '')
        if key in seen:
            continue
        seen.add(key)
        result.append({'de': key[0], 'ru': key[1]})
    return result


def generate_word_family(word, usage, part):
    items = []
    translations = usage.get('translations') or set()
    translation_hint = next(iter(translations), '')
    if part == 'существительное':
        items.append(f"Основа: {word}")
        items.append(f"Множественное число (пример): {guess_plural(word, usage.get('gender'))}")
        base = word.split(' ', 1)[1] if word.startswith(('der ', 'die ', 'das ')) else word
        if translation_hint:
            items.append(f"Семейство значений: {translation_hint}")
        else:
            items.append(f"Связанный корень: {base}")
    elif part == 'глагол':
        items.append(f"Инфинитив: {word}")
        items.append(f"Презенс: {conjugate_ich(word)}")
        if translation_hint:
            items.append(f"Совершенный оттенок: завершённое действие «{translation_hint}»")
        else:
            items.append("Совершенный оттенок: действие доведено до конца")
    elif part == 'прилагательное':
        items.append(f"Основная форма: {word}")
        items.append(f"Сравнительная степень: {comparative_form(word)}")
        items.append(f"Превосходная степень: {superlative_form(word)}")
    else:
        items.append(f"Ключевая форма: {word}")
    return unique_strings(items)


def generate_collocations(usage):
    collocations = []
    for de, ru in usage['examples']:
        if de and ru:
            collocations.append(f"{de} — {ru}")
        elif de:
            collocations.append(de)
    if not collocations:
        translation = next(iter(usage['translations']), '')
        if translation:
            collocations.append(f"В контексте: {translation}")
    return unique_strings(collocations)


def generate_synonyms(word, usage, part, token_map):
    synonyms = []
    tokens = []
    for translation in usage['translations']:
        tokens.extend(tokenize_translation(translation))
    for token in tokens:
        synonyms.append(token)
        related = [w for w in sorted(token_map[token.lower()]) if w != word]
        for other in related[:2]:
            synonyms.append(f"{other} — тоже «{token}»")
    if not synonyms:
        translation = next(iter(usage['translations']), '')
        if translation:
            if part == 'глагол':
                synonyms.append(f"похоже на действие: {translation}")
            elif part == 'существительное':
                synonyms.append(f"родственное понятие: {translation}")
            else:
                synonyms.append(f"схожее качество: {translation}")
    return unique_strings(synonyms)


def build_usage(vocab_data, characters):
    usage_map = {}
    for entry in vocab_data.get('vocabulary', []):
        german = entry.get('german')
        if not german:
            continue
        usage = ensure_usage(usage_map, german)
        translation = entry.get('translation')
        if translation:
            usage['translations'].add(translation)
        transcription = entry.get('transcription')
        if transcription:
            usage['transcriptions'].add(transcription)
        part = entry.get('part_of_speech')
        if part:
            usage['part_of_speech'] = part
        gender = entry.get('gender')
        if gender:
            usage['gender'] = gender
        level = entry.get('level')
        if level:
            usage['levels'].add(level)
        for theme in entry.get('themes', []) or []:
            usage['themes'].add(theme)
        for sample in entry.get('example_sentences', []):
            de = sample.get('de')
            ru = sample.get('ru')
            usage['examples'].append((de or '', ru or ''))
    for char in characters:
        char_id = char.get('id') or char.get('name') or ''
        for phase in char.get('journey_phases', []):
            phase_id = phase.get('id') or ''
            phase_key = f"{char_id}:{phase_id}" if char_id and phase_id else char_id or phase_id
            keywords = phase.get('keywords') or ''
            keyword_tokens = [token.strip() for token in re.split(r'\s*[•,;/]+\s*', keywords) if token.strip()]
            for vocab in phase.get('vocabulary', []):
                german = vocab.get('german')
                if not german:
                    continue
                usage = ensure_usage(usage_map, german)
                translation = vocab.get('russian')
                if translation:
                    usage['translations'].add(translation)
                transcription = vocab.get('transcription')
                if transcription:
                    usage['transcriptions'].add(transcription)
                sentence = vocab.get('sentence')
                sentence_translation = vocab.get('sentence_translation')
                if sentence or sentence_translation:
                    usage['examples'].append((sentence or '', sentence_translation or ''))
                usage['characters'].add(phase_key)
                for kw in keyword_tokens:
                    usage['keywords'].add(kw)
    return usage_map


def enrich_vocabulary():
    vocab_data, characters = load_data()
    usage_map = build_usage(vocab_data, characters)

    token_map = defaultdict(set)
    for word, usage in usage_map.items():
        for translation in usage['translations']:
            for token in tokenize_translation(translation):
                token_map[token.lower()].add(word)

    existing_entries = {entry.get('german'): entry for entry in vocab_data.get('vocabulary', []) if entry.get('german')}

    max_id = 0
    max_rank = 0
    for entry in vocab_data.get('vocabulary', []):
        word_id = entry.get('id', '')
        if word_id.startswith('word_'):
            try:
                num = int(word_id.split('_')[1])
            except ValueError:
                continue
            max_id = max(max_id, num)
        rank = entry.get('frequency_rank')
        if isinstance(rank, int):
            max_rank = max(max_rank, rank)

    updated_entries = []

    for german in sorted(usage_map.keys(), key=lambda x: x.lower()):
        usage = usage_map[german]
        entry = existing_entries.get(german)
        part = detect_part_of_speech(german, usage)
        translations = ', '.join(sorted(usage['translations']))
        transcription = next(iter(usage['transcriptions']), '')
        examples = unique_examples(usage['examples'])
        word_family = generate_word_family(german, usage, part)
        collocations = generate_collocations(usage)
        synonyms = generate_synonyms(german, usage, part, token_map)
        if entry:
            entry['translation'] = translations or entry.get('translation', '')
            if transcription:
                entry['transcription'] = transcription
            entry['part_of_speech'] = part
            if not entry.get('level') and usage['levels']:
                entry['level'] = sorted(usage['levels'])[0]
            if usage['themes']:
                entry['themes'] = sorted(usage['themes'])
            entry['example_sentences'] = examples or entry.get('example_sentences', [])
        else:
            max_id += 1
            max_rank += 1
            entry = {
                'id': f'word_{max_id:04d}',
                'german': german,
                'german_stressed': german,
                'transcription': transcription,
                'translation': translations,
                'part_of_speech': part,
                'level': 'B1',
                'frequency_rank': max_rank,
                'themes': sorted(usage['keywords']) or ['король лир'],
                'example_sentences': examples,
                'word_family': [],
                'synonyms': [],
                'collocations': [],
            }
        entry['word_family'] = word_family
        entry['synonyms'] = synonyms
        entry['collocations'] = collocations
        updated_entries.append(entry)

    vocab_data['vocabulary'] = updated_entries
    vocab_data.setdefault('metadata', {})['total_words'] = len(updated_entries)

    with VOCAB_PATH.open('w', encoding='utf-8') as fp:
        json.dump(vocab_data, fp, ensure_ascii=False, indent=2)
    print(f"Updated vocabulary with {len(updated_entries)} entries")


if __name__ == '__main__':
    enrich_vocabulary()
