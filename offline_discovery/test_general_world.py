import unittest
from offline_discovery.general_world import run


class GeneralWorldDiscoveryTest(unittest.TestCase):
    def test_discovers_and_generalizes(self):
        result = run()
        self.assertTrue(result["network_isolated"])
        self.assertTrue(result["verified"])
        self.assertEqual(result["predictions"], [11, 7, -37, 0])
        self.assertEqual(result["expected"], [11, 7, -37, 0])
        self.assertEqual(result["max_error"], 0)
        self.assertEqual(result["discovered_expression"], "5*1 + 1*x*t + 1*2t-3x")


if __name__ == "__main__":
    unittest.main()
