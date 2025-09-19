"""Unit tests for the Lira JavaScript generator."""

import json
import unittest

from generators.js_lira import LiraJSGenerator


class LiraJSGeneratorTests(unittest.TestCase):
    """Verify special character handling in generated JavaScript."""

    def test_generate_handles_quotes_and_newlines(self):
        """The generator should preserve special characters in JSON output."""

        character_data = {
            'journey_phases': [
                {
                    'id': 'phase1',
                    'title': "Эдмунд's \"choice\"",
                    'description': 'Первая строка\nВторая строка',
                    'vocabulary': [
                        {
                            'german': 'die Entscheidung',
                            'russian': 'решение',
                            'transcription': '[энт-ШАЙ-дӯнг]',
                    'sentence': 'Er flüstert: "Das ist Edmunds Weg."\nUnd geht.',
                    'sentence_translation': 'Он шепчет: "Это путь Эдмунда."\nИ уходит.',
                    'sentence_parts': ['Er flüstert: "', '"\nUnd geht.'],
                            'visual_hint': '🎯',
                            'themes': ['Strategie', 'Täuschung'],
                        }
                    ],
                }
            ]
        }

        script = LiraJSGenerator.generate(character_data)

        # Extract JSON portion of the script and validate it can round-trip
        self.assertIn('const phaseVocabularies = ', script)
        separator = ';' + '\n' * 2
        self.assertIn(separator, script)
        json_part, remainder = script.split(separator, 1)
        json_str = json_part.replace('const phaseVocabularies = ', '', 1)
        payload = json.loads(json_str)

        self.assertIn('phase1', payload)

        phase_payload = payload['phase1']
        self.assertEqual(phase_payload['title'], character_data['journey_phases'][0]['title'])
        self.assertEqual(
            phase_payload['description'],
            character_data['journey_phases'][0]['description'],
        )

        [word_payload] = phase_payload['words']
        [word_source] = character_data['journey_phases'][0]['vocabulary']

        self.assertEqual(word_payload['word'], word_source['german'])
        self.assertEqual(word_payload['translation'], word_source['russian'])
        self.assertEqual(word_payload['transcription'], word_source['transcription'])
        self.assertEqual(word_payload['sentence'], word_source['sentence'])
        self.assertEqual(
            word_payload['sentenceTranslation'],
            word_source['sentence_translation'],
        )
        self.assertEqual(word_payload['visual_hint'], word_source['visual_hint'])
        self.assertEqual(word_payload['themes'], word_source['themes'])
        self.assertEqual(word_payload['sentenceParts'], word_source['sentence_parts'])

        self.assertIn('constructorItems', phase_payload)
        self.assertEqual(len(phase_payload['constructorItems']), 1)
        constructor_item = phase_payload['constructorItems'][0]
        self.assertEqual(constructor_item['word'], word_source['german'])
        self.assertEqual(constructor_item['sentenceParts'], word_source['sentence_parts'])

        self.assertIn('const phaseConstructorData = ', script)
        constructor_part, _ = remainder.split(separator, 1)
        constructor_json = constructor_part.replace('const phaseConstructorData = ', '', 1)
        constructor_payload = json.loads(constructor_json)

        self.assertIn('phase1', constructor_payload)
        self.assertEqual(constructor_payload['phase1'], phase_payload['constructorItems'])

        # ensure_ascii=False keeps non-latin characters intact in the script output
        self.assertIn('решение', script)


if __name__ == '__main__':
    unittest.main()
