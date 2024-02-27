import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from tkinter import Tk
import dns
from web_enumeration_tool import WebEnumerationTool  # Replace 'your_module' with the actual module name

class TestWebEnumerationTool(unittest.TestCase):
    def setUp(self):
        self.root = Tk()

    def tearDown(self):
        self.root.destroy()

    @patch('tkinter.messagebox.showerror')
    def test_dns_enumeration_exception_handling(self, mock_showerror):
        tool = WebEnumerationTool(self.root)
        with patch('dns.resolver.resolve', side_effect=dns.resolver.NXDOMAIN):
            tool.enumerate_target('example.com')
        mock_showerror.assert_called_once_with('Error', 'The DNS query name does not exist. Please check the entered URL.')

    @patch('tkinter.messagebox.showerror')
    def test_general_exception_handling(self, mock_showerror):
        tool = WebEnumerationTool(self.root)
        with patch('dns.resolver.resolve', side_effect=Exception('Some error')):
            tool.enumerate_target('example.com')
        mock_showerror.assert_called_once_with('Error', 'An error occurred: Some error')

    @patch('requests.get')
    @patch('dns.resolver.resolve')
    def test_enumerate_target(self, mock_dns_resolve, mock_requests_get):
        tool = WebEnumerationTool(self.root)
        mock_dns_resolve.return_value = [MagicMock(address='127.0.0.1')]
        mock_requests_get.return_value.headers = {'Server': 'TestServer'}
        with patch.object(tool, 'ip_address_information') as mock_ip_info, \
             patch.object(tool, 'web_server_information') as mock_web_server_info, \
             patch.object(tool, 'directory_file_enumeration') as mock_directory_info:
            tool.enumerate_target('example.com')

            mock_ip_info.assert_called_once_with('example.com')
            mock_web_server_info.assert_called_once_with('example.com')
            mock_directory_info.assert_called_once_with('example.com')

    # Add more test cases for other methods as needed

if __name__ == '__main__':
    unittest.main()
