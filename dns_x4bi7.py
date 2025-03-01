  GNU nano 8.3                                                                                                                                                                                                                  dns.py                                                                                                                                                                                                                            import subprocess
import os
import threading
from queue import Queue
from termcolor import colored

# Clear screen
os.system('clear')

# ASCII Banner with color
BANNER = colored("""
▒██   ██▒    ▄▄▄          ▄▄▄▄       ██▓   ▄▄▄█████▓
▒▒ █ █ ▒░   ▒████▄       ▓█████▄    ▓██▒   ▓  ██▒ ▓▒
░░  █   ░   ▒██  ▀█▄     ▒██▒ ▄██   ▒██▒   ▒ ▓██░ ▒░
 ░ █ █ ▒    ░██▄▄▄▄██    ▒██░█▀     ░██░   ░ ▓██▓ ░
▒██▒ ▒██▒    ▓█   ▓██▒   ░▓█  ▀█▓   ░██░     ▒██▒ ░
▒▒ ░ ░▓ ░    ▒▒   ▓▒█░   ░▒▓███▀▒   ░▓       ▒ ░░
░░   ░▒ ░     ▒   ▒▒ ░   ▒░▒   ░     ▒ ░       ░
 ░    ░       ░   ▒       ░    ░     ▒ ░     ░
 ░    ░           ░  ░    ░          ░
                               ░
""", "red") + colored("""
Author: XABIT | Bug Bounty (DNS Zone Transfer)
==============================================
""", "cyan")
print(BANNER)

def get_ns_records(subdomain):
    try:
        result = subprocess.run(["dig", subdomain, "-t", "NS", "+short"], capture_output=True, text=True)
        ns_records = result.stdout.strip().split("\n")
        return [ns for ns in ns_records if ns]
    except Exception as e:
        print(colored(f"Error fetching NS records for {subdomain}: {e}", "yellow"))
        return []

def attempt_zone_transfer(subdomain, ns_servers):
    for ns in ns_servers:
        try:
            result = subprocess.run(["dig", "@" + ns, subdomain, "AXFR"], capture_output=True, text=True)
            output = result.stdout.strip()

            if "Transfer failed" not in output and output and "failed" not in output.lower() and "no servers could be reached" not in output.lower():
                print(colored(f"\n--- Zone Transfer Successful for {subdomain} using NS {ns} ---\n", "green"))
                with open("zone.txt", "w") as f_out:
                    f_out.write(output + "\n")
                return True
            else:
                print(colored(f"Zone Transfer failed for {subdomain} using NS {ns}", "yellow"))
        except Exception as e:
            print(colored(f"Error attempting zone transfer for {subdomain} using {ns}: {e}", "yellow"))
    return False

def worker(queue):
    while not queue.empty():
        subdomain = queue.get()
        ns_records = get_ns_records(subdomain)
        if ns_records:
            if attempt_zone_transfer(subdomain, ns_records):
                print(colored("\nZone Transfer completed successfully. Stopping further scans.", "cyan"))
                return
        else:
            print(colored(f"No NS records found for {subdomain}", "yellow"))
        queue.task_done()

def main():
    input_file = input(colored("Enter the subdomains file path: ", "cyan"))

    try:
        with open(input_file, "r") as f:
            subdomains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(colored(f"Error: {input_file} not found!", "yellow"))
        return

    queue = Queue()
    for subdomain in subdomains:
        queue.put(subdomain)

    threads = []
    for _ in range(100):  # 100 threads for faster execution
        thread = threading.Thread(target=worker, args=(queue,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(colored("\nNo successful Zone Transfers found.", "red"))

if __name__ == "__main__":
    main()
