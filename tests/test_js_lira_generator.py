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
        json_part, _ = script.split(separator, 1)
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

        # ensure_ascii=False keeps non-latin characters intact in the script output
        self.assertIn('решение', script)


if __name__ == '__main__':
    unittest.main()
