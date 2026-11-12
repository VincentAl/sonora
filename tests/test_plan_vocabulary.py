import datetime as dt
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from plan_vocabulary import plan


class VocabularyPlannerTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            {'id': 'a', 'es': 'a', 'fr_sense': 'a', 'status': 'candidate', 'priority': 5},
            {'id': 'b', 'es': 'b', 'fr_sense': 'b', 'status': 'candidate', 'priority': 4},
            {'id': 'c', 'es': 'c', 'fr_sense': 'c', 'status': 'candidate', 'priority': 3},
            {'id': 'd', 'es': 'd', 'fr_sense': 'd', 'status': 'retired', 'priority': 5},
        ]
        self.today = dt.date(2026, 11, 2)

    def test_draft_is_reserved_not_learned(self):
        h = [{'target_id': 'a', 'date': '2026-10-01', 'stage': 'draft'}]
        result = plan(self.items, h, self.today, limit=2)
        self.assertEqual([(x['id'], x['reason']) for x in result['proposed']], [('b', 'new'), ('c', 'new')])
        self.assertEqual(result['pending_excluded'], ['a'])

    def test_recent_published_is_excluded(self):
        h = [{'target_id': 'a', 'date': '2026-10-30', 'stage': 'published'}]
        self.assertEqual([x['id'] for x in plan(self.items, h, self.today, limit=3)['proposed']], ['b', 'c'])

    def test_published_after_draft_unreserves_for_revisit(self):
        h = [{'target_id': 'b', 'date': '2026-09-30', 'stage': 'draft'},
             {'target_id': 'b', 'date': '2026-10-01', 'stage': 'published'}]
        result = plan(self.items, h, self.today, limit=2)
        self.assertEqual(result['proposed'][0]['id'], 'b')
        self.assertNotIn('b', result['pending_excluded'])

    def test_spaced_revisit_is_selected(self):
        h = [{'target_id': 'b', 'date': '2026-10-01', 'stage': 'published'}]
        result = plan(self.items, h, self.today, limit=2, revisit_slots=1)
        self.assertEqual([(x['id'], x['reason']) for x in result['proposed']], [('b', 'revisit'), ('a', 'new')])

    def test_reproducible_and_retired_excluded(self):
        a = plan(self.items, [], self.today, limit=4)
        self.assertEqual(a, plan(self.items, [], self.today, limit=4))
        self.assertEqual([x['id'] for x in a['proposed']], ['a', 'b', 'c'])

    def test_reject_unknown_history_and_future_publication(self):
        with self.assertRaises(ValueError):
            plan(self.items, [{'target_id': 'z', 'date': '2026-10-01', 'stage': 'published'}], self.today)
        with self.assertRaises(ValueError):
            plan(self.items, [{'target_id': 'a', 'date': '2026-11-03', 'stage': 'published'}], self.today)

    def test_reject_unknown_stage(self):
        with self.assertRaises(ValueError):
            plan(self.items, [{'target_id': 'a', 'date': '2026-10-01', 'stage': 'listened'}], self.today)

    def test_diagnostic_blocks_known_and_unverified_candidates(self):
        items = [
            {'id': 'known', 'es': 'atreverse', 'fr_sense': 'oser', 'status': 'candidate', 'priority': 5},
            {'id': 'unverified', 'es': 'hallar', 'fr_sense': 'trouver', 'status': 'candidate', 'priority': 5},
            {'id': 'learn', 'es': 'no pegar ojo', 'fr_sense': 'ne pas dormir', 'status': 'learning', 'priority': 4},
        ]
        diagnostic = {'known': ['atreverse'], 'learning': ['no pegar ojo']}
        result = plan(items, [], self.today, limit=5, diagnostic=diagnostic)
        self.assertEqual([x['es'] for x in result['proposed']], ['no pegar ojo'])

    def test_diagnostic_rejects_overlap(self):
        with self.assertRaises(ValueError):
            plan(self.items, [], self.today, diagnostic={'known': ['a'], 'learning': ['a']})

    def test_reject_duplicate_ids(self):
        with self.assertRaises(ValueError):
            plan(self.items + [self.items[0]], [], self.today)


if __name__ == '__main__':
    unittest.main()
