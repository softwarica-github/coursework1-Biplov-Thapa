import argparse
import socket
import dns.resolver
from bs4 import BeautifulSoup
import requests
import concurrent.futures

class WebEnumerationToolCLI:
    def __init__(self, target_url):
        self.target_url = target_url

    def start_enumeration(self):
        try:
            # Perform enumeration tasks (e.g., DNS, IP, Web Server, etc.)
            dns_result = self.dns_enumeration(self.target_url)
            ip_result = self.ip_address_information(self.target_url)
            web_server_result = self.web_server_information(self.target_url)
            directory_result = self.directory_file_enumeration(self.target_url)

            # Display results in the CLI
            results = f"DNS Result: {dns_result}\nIP Result: {ip_result}\nWeb Server Result: {web_server_result}\nDirectory Result: {directory_result}"
            print(results)

        except dns.resolver.NXDOMAIN:
            print("Error: The DNS query name does not exist. Please check the entered URL.")
        except Exception as e:
            print(f"Error: An error occurred - {e}")

    def dns_enumeration(self, target_url):
        result = dns.resolver.resolve(target_url, 'A')
        return [ip.address for ip in result]

    def ip_address_information(self, target_url):
        ip_address = socket.gethostbyname(target_url)
        return f'Resolved IP Address: {ip_address}'

    def web_server_information(self, target_url):
        response = requests.get(f'http://{target_url}')
        return f'Web Server: {response.headers.get("Server", "Unknown")}'

    def directory_file_enumeration(self, target_url):
        response = requests.get(f'http://{target_url}')
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a', href=True)]
        return f'Discovered Links: {links}'


def main():
    parser = argparse.ArgumentParser(description="Web Enumeration Tool CLI")
    parser.add_argument("target_url", help="Target URL or IP address to enumerate")
    args = parser.parse_args()

    web_enumerator = WebEnumerationToolCLI(args.target_url)
    web_enumerator.start_enumeration()

if __name__ == "__main__":
    main()
