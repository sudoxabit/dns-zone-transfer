**DNS Zone Transfer Scanner**  

This Python script automates the process of testing for DNS Zone Transfer vulnerabilities across multiple subdomains. It uses `dig` to retrieve NS (Name Server) records and attempts an AXFR (Zone Transfer) request to extract DNS records. The script supports multithreading for faster execution and logs successful zone transfers to `zone.txt`.  

### Features:  
- Retrieves NS records for subdomains.  
- Attempts DNS Zone Transfer (AXFR) attacks.  
- Uses multithreading (100 threads) for efficient scanning.  
- Saves successful zone transfers to a file.  
- Displays colored terminal output for better readability.  

🔹 **Author**: XABIT  
🔹 **Usage**: Run the script and provide a file containing a list of subdomains. The script will test each for a possible zone transfer vulnerability.  

🚀 **For ethical security testing and bug bounty research only!**
