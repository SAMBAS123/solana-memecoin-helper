import unittest
from unittest.mock import patch
from scanner import fast_memecoin_scan

class TestFastMemecoinScan(unittest.TestCase):
    @patch('scanner.scan_holders')
    @patch('scanner.get_swap_route')
    @patch('scanner.send_alert')
    def test_risky_bundle_ratio_alert(self, mock_alert, mock_route, mock_holders):
        mock_holders.return_value = [{"address": "whale1", "percentage": 10}]
        mock_route.return_value = {"bundle_ratio": 2, "liq_alpha": "Dump risk"}
        result = fast_memecoin_scan("test_token", mc_threshold=15000)
        mock_alert.assert_called_with("Risky bundle ratio for test_token")
        self.assertEqual(result["alpha"], "Dump risk")

if __name__ == '__main__':
    unittest.main()
