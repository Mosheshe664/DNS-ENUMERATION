# DNS-ENUMERATION
This Python script automates reconnaissance tasks on a target domain by discovering subdomains, identifying which ones are live, and scanning them for open ports using Nmap. The final results are written to a report file for easy reference.


The features are as follows
* Subdomain Enumeration via dnsrecon

* Live Subdomain Detection using HTTP/HTTPS requests

* Open Port Scanning with nmap

* Saves output in a structured Markdown report

  
Make sure the following tools and libraries are installed on your system
* dns recon
* nmap

  
How it works
Subdomain Enumeration:
The script uses dnsrecon to find subdomains of the specified target domain.

Liveness Check:
It attempts HTTP and HTTPS connections to each subdomain to check which ones are alive.

Port Scanning:
Each live subdomain is scanned using nmap to find open ports.

Report Generation:
The results are saved in a file named open_ports_report.txt in Markdown format

How to use it
1. Edit the Target Domain
Open the script in any text editor and set the target domain:
*TARGET_DOMAIN = "example.com"
Alternatively, you can modify the script to ask for user input (already prepared if you'd prefer that version).

2. Run the Script
**python3 script_name.py
Replace script_name.py with the actual filename you saved the script as.

3. View the Results
After execution, open open_ports_report.txt to see the structured list of live subdomains and their open ports.

The output will look something like this
# Open Port Report for example.com

## sub1.example.com
PORT     STATE SERVICE
80/tcp   open  http
443/tcp  open  https

## sub2.example.com
PORT     STATE SERVICE
22/tcp   open  ssh
