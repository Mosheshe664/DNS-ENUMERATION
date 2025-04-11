import subprocess
import re
import requests
from concurrent.futures import ThreadPoolExecutor

TARGET_DOMAIN = "target domain"
OUTPUT_FILE = "open_ports_report.txt"

def run_dnsrecon(domain):
    print(f"[*] Running dnsrecon on {domain}...")
    try:
        result = subprocess.run(
            ["dnsrecon", "-d", domain, "-t", "std"],
            capture_output=True, text=True
        )
        output = result.stdout
        subdomains = re.findall(r"A\s+([a-zA-Z0-9.-]+)\s", output)
        return list(set(subdomains))
    except Exception as e:
        print(f"[!] Error running dnsrecon: {e}")
        return []

def is_live(subdomain):
    for scheme in ['http://', 'https://']:
        try:
            r = requests.head(scheme + subdomain, timeout=3, allow_redirects=True)
            if r.status_code < 400:
                return True
        except:
            continue
    return False

def filter_live_subdomains(subdomains):
    print("[*] Checking which subdomains are live...")
    live = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda s: (s, is_live(s)), subdomains))
    for sub, status in results:
        if status:
            print(f"[+] Live: {sub}")
            live.append(sub)
    return live

def scan_with_nmap(subdomain):
    print(f"[*] Scanning {subdomain} with nmap...")
    try:
        result = subprocess.run(
            ["nmap", "-Pn", "-T4", subdomain],
            capture_output=True, text=True
        )
        return result.stdout
    except Exception as e:
        return f"[!] Error scanning {subdomain} with nmap: {e}"

def save_results(results, file_path):
    with open(file_path, "w") as f:
        f.write(results)
    print(f"[*] Results saved to {file_path}")

def main():
    all_subdomains = run_dnsrecon(TARGET_DOMAIN)
    print(f"[*] Found {len(all_subdomains)} subdomains.")

    live_subdomains = filter_live_subdomains(all_subdomains)
    print(f"[*] {len(live_subdomains)} subdomains are live.")

    final_report = f"# Open Port Report for {TARGET_DOMAIN}\n\n"

    for sub in live_subdomains:
        scan_result = scan_with_nmap(sub)
        final_report += f"\n## {sub}\n{scan_result}\n"

    save_results(final_report, OUTPUT_FILE)

if __name__ == "__main__":
    main()
