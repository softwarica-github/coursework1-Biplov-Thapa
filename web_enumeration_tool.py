import requests
import socket
import dns.resolver
from bs4 import BeautifulSoup
import concurrent.futures
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
import threading

class WebEnumerationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Enumeration Tool")

        # Create tabs
        self.tabControl = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Enumeration')
        self.tabControl.add(self.tab2, text='Results')
        self.tabControl.pack(expand=1, fill="both")

        # Enumeration Tab
        self.create_enumeration_tab()

        # Results Tab
        self.create_results_tab()

    def create_enumeration_tab(self):
        self.lbl_target = tk.Label(self.tab1, text="Target URL or IP:")
        self.lbl_target.grid(column=0, row=0, padx=10, pady=10)

        self.target_entry = tk.Entry(self.tab1, width=30)
        self.target_entry.grid(column=1, row=0, padx=10, pady=10)

        self.enumerate_button = tk.Button(self.tab1, text="Enumerate", command=self.start_enumeration)
        self.enumerate_button.grid(column=2, row=0, padx=10, pady=10)

        self.progress_bar = ttk.Progressbar(self.tab1, mode="indeterminate")
        self.progress_bar.grid(column=0, row=1, columnspan=3, pady=10)

    def create_results_tab(self):
        self.results_text = tk.Text(self.tab2, height=20, width=50)
        self.results_text.grid(column=0, row=0, padx=10, pady=10)

    def start_enumeration(self):
        target_url = self.target_entry.get()
        self.results_text.delete(1.0, tk.END)  # Clear previous results
        self.progress_bar.start()

        # Start enumeration in a separate thread
        enumeration_thread = threading.Thread(target=self.enumerate_target, args=(target_url,))
        enumeration_thread.start()

    def enumerate_target(self, target_url):
        try:
            # Perform enumeration tasks (e.g., DNS, IP, Web Server, etc.)
            dns_result = self.dns_enumeration(target_url)
            ip_result = self.ip_address_information(target_url)
            web_server_result = self.web_server_information(target_url)
            directory_result = self.directory_file_enumeration(target_url)

            # Display results in the GUI
            results = f"DNS Result: {dns_result}\nIP Result: {ip_result}\nWeb Server Result: {web_server_result}\nDirectory Result: {directory_result}"
            self.results_text.insert(tk.END, results)

        except dns.resolver.NXDOMAIN:
            messagebox.showerror("Error", "The DNS query name does not exist. Please check the entered URL.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        finally:
            self.progress_bar.stop()

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
    root = tk.Tk()
    app = WebEnumerationTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
