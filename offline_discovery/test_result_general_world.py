import unittest
from offline_discovery.general_world import run


class ResultRegressionTest(unittest.TestCase):
    def test_verified_result(self):
        r = run()
        self.assertEqual(r['predictions'], [11, 7, -37, 0])
        self.assertEqual(r['expected'], [11, 7, -37, 0])
        self.assertEqual(r['max_error'], 0)
        self.assertTrue(r['verified'])

if __name__ == '__main__':
    unittest.main()
