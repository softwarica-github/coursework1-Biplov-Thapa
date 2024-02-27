import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from web_enumeration_tool import WebEnumerationTool
import dns

class TestWebEnumerationToolIntegration(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()

    def tearDown(self):
        self.root.destroy()

    @patch('web_enumeration_tool.dns.resolver.resolve')
    @patch('web_enumeration_tool.socket.gethostbyname')
    @patch('web_enumeration_tool.requests.get')
    @patch('web_enumeration_tool.requests.models.Response')
    def test_enumerate_target_integration(self, mock_response, mock_requests_get, mock_gethostbyname, mock_dns_resolve):
        # Set up mock responses for DNS and HTTP requests
        mock_dns_resolve.return_value = [MagicMock(address='127.0.0.1')]
        mock_gethostbyname.return_value = '127.0.0.1'

        # Create an instance of the WebEnumerationTool
        tool = WebEnumerationTool(self.root)

        # Simulate user input
        tool.target_entry.insert(0, 'example.com')

        # Trigger enumeration
        tool.start_enumeration()

        # Assert that DNS resolution, IP address information, and web server information were called with the correct arguments
        mock_dns_resolve.assert_called_once_with('example.com', 'A')
        mock_gethostbyname.assert_called_once_with('example.com')
        mock_requests_get.assert_called_once_with('http://example.com')

        # Simulate mock response for HTTP request
        mock_response.headers = {'Server': 'TestServer'}
        mock_response.text = '<a href="/link1">Link 1</a><a href="/link2">Link 2</a>'
        mock_requests_get.return_value = mock_response

        # Check if the results were displayed correctly in the GUI
        expected_results = "DNS Result: ['127.0.0.1']\nIP Result: Resolved IP Address: 127.0.0.1\nWeb Server Result: Web Server: TestServer\nDirectory Result: Discovered Links: ['/link1', '/link2']"
        self.assertEqual(tool.results_text.get("1.0", "end").strip(), expected_results)

if __name__ == '__main__':
    unittest.main()
