import importlib.util, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("analysis",Path(__file__).resolve().parents[1]/"analysis.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class AuditTests(unittest.TestCase):
    def test_published_trial_transcription(self):
        r=m.analyse()["real_trials"]
        self.assertEqual(r["successes"],{"base_success":0,"libero_success":7,"pear_success":18})
        self.assertEqual(r["final_failures"],{"unaligned":3,"round_budget":6,"toppled":2,"rolled_away":1})
        self.assertEqual(r["libero_to_final"],{"both_success":5,"new_success":13,"lost_success":2})
    def test_workload_endpoints_and_crossover(self):
        p=m.crossover(74.4,57.4,96.9,.75)
        self.assertAlmostEqual(m.mixture(p,74.4,57.4),m.mixture(p,96.9,.75))
        self.assertEqual(m.mixture(0,74.4,57.4),74.4)
        self.assertEqual(m.mixture(1,74.4,57.4),57.4)
    def test_wilson_known_case_and_invalid_counts(self):
        low,high=m.wilson(18,30)
        self.assertAlmostEqual(low,42.32,places=1);self.assertAlmostEqual(high,75.41,places=1)
        with self.assertRaises(ValueError):m.wilson(1,0)
    def test_macro_is_not_micro(self):
        r=m.analyse()["full_robodojo"]
        self.assertAlmostEqual(r["micro_percent"],3.8888888889)
        self.assertNotEqual(r["micro_percent"],r["reported_dimension_macro_percent"])
if __name__=="__main__":unittest.main()

