import unittest
from unittest.mock import patch, MagicMock
from pulsecot.functions import get_agency_info


class TestGetAgencyInfo(unittest.TestCase):
    @patch("urllib.request.urlopen")
    @patch("pulsecot.gnu.decode_pulse")
    @patch("json.loads")
    def test_get_agency_info_success(
        self, mock_json_loads, mock_decode_pulse, mock_urlopen
    ):
        # Mock the response from urllib.request.urlopen
        mock_response = MagicMock()
        mock_response.read.return_value = (
            b'{"agencies": [{"id": "123", "name": "Test Agency"}]}'
        )
        mock_urlopen.return_value = mock_response

        # Mock the JSON and decode_pulse behavior
        mock_json_loads.return_value = {
            "agencies": [{"id": "123", "name": "Test Agency"}]
        }
        mock_decode_pulse.return_value = {
            "agencies": [{"id": "123", "name": "Test Agency"}]
        }

        # Call the function
        agency_info = get_agency_info("123")

        # Assertions
        self.assertIsNotNone(agency_info)
        self.assertEqual(agency_info["id"], "123")
        self.assertEqual(agency_info["name"], "Test Agency")

    @patch("urllib.request.urlopen")
    def test_get_agency_info_no_content(self, mock_urlopen):
        # Mock the response from urllib.request.urlopen with no content
        mock_response = MagicMock()
        mock_response.read.return_value = b""
        mock_urlopen.return_value = mock_response

        # Call the function
        agency_info = get_agency_info("123")

        # Assertions
        self.assertIsNone(agency_info)

    @patch("urllib.request.urlopen")
    @patch("json.loads")
    def test_get_agency_info_invalid_data(self, mock_json_loads, mock_urlopen):
        # Mock the response from urllib.request.urlopen
        mock_response = MagicMock()
        mock_response.read.return_value = b"{}"
        mock_urlopen.return_value = mock_response

        # Mock the JSON behavior
        mock_json_loads.return_value = {}

        # Call the function
        agency_info = get_agency_info("123")

        # Assertions
        self.assertIsNone(agency_info)


if __name__ == "__main__":
    unittest.main()
