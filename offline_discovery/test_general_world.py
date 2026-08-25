import unittest
from offline_discovery.general_world import run


class GeneralWorldDiscoveryTest(unittest.TestCase):
    def test_discovers_and_generalizes(self):
        result = run()
        self.assertTrue(result["network_isolated"])
        self.assertTrue(result["verified"])
        self.assertEqual(result["predictions"], result["expected"])
        self.assertEqual(result["max_error"], 0)


if __name__ == "__main__":
    unittest.main()
