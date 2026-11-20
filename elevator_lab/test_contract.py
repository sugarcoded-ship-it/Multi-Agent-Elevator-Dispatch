"""Policy-neutral checks. Different justified preferences can pass."""
import unittest
from unittest.mock import patch
from models import Elevator, Request, Decision
from rules import eligible_ids
from scenarios import SCENARIOS
import dispatcher
import app

class DispatchContract(unittest.TestCase):
    def test_eligible_choice_and_reason(self):
        case = SCENARIOS[0]
        result = dispatcher.choose_elevator(case.elevators, case.request)
        self.assertIsInstance(result, Decision)
        self.assertIn(result.elevator_id, eligible_ids(case.elevators, case.request))
        self.assertIsInstance(result.reason, str)
        self.assertTrue(result.reason.strip())

    def test_full_car_is_excluded(self):
        case = SCENARIOS[3]
        self.assertEqual(dispatcher.choose_elevator(case.elevators, case.request).elevator_id, "B")

    def test_no_eligible_car(self):
        case = SCENARIOS[4]
        result = dispatcher.choose_elevator(case.elevators, case.request)
        self.assertIsNone(result.elevator_id)
        self.assertTrue(result.reason.strip())

    def test_repeatable_and_unchanged(self):
        case = SCENARIOS[0]
        before = repr(case)
        first = dispatcher.choose_elevator(case.elevators, case.request)
        self.assertEqual(dispatcher.choose_elevator(case.elevators, case.request), first)
        self.assertEqual(repr(case), before)

class AppContract(unittest.TestCase):
    def test_calls_and_displays(self):
        cases = [SCENARIOS[0], SCENARIOS[4]]
        decisions = [Decision("A", "EXAMPLE_REASON_ONE"), Decision(None, "EXAMPLE_REASON_TWO")]
        output = []
        with patch("app.choose_elevator", side_effect=decisions) as choose:
            actual = app.run_scenarios(cases, output.append)
        self.assertEqual(actual, decisions)
        self.assertEqual(choose.call_count, 2)
        for call, case in zip(choose.call_args_list, cases):
            self.assertEqual(call.args, (case.elevators, case.request))
        display = "\n".join(output)
        for case in cases:
            self.assertIn(case.name, display)
        self.assertIn("Selected: A", display)
        self.assertIn("Selected: WAIT", display)
        for decision in decisions:
            self.assertIn(decision.reason, display)

    def test_empty_display(self):
        self.assertEqual(app.run_scenarios([], lambda text: None), [])

if __name__ == "__main__":
    unittest.main()
