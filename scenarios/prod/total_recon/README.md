# scenario-total-recon
Graduated Recon Port Scanning Scenario for EDURange cybersecurity training platform.

## Running

You can run the scenario using the `terraform` command line tool.
```
terraform init
terraform apply
```
Then to clean up:
```
terraform destroy
```

## Instances

### Home Subnet

1. Home
 - Port scan Rekall's ip to get non-standard ssh port, then ssh -p to host

### Earth Subnet

2. Rekall
 - Scan small subnet 10.0.0.0/24 to find the nearest host, then ssh to that host

3. Warehouse
 - Look for a host on the subnet that is blocking pings -- ssh to that host

4. Earth_Aerospace_Port
 - Fast scan the subnet for 10.0.192.0/18 -- ssh to the first host that ends in 33

### Mars Subnet

5. Mars_Aerospace_Port
 - Venusville's ssh port is open, but it's been changed to an arbitrary port (123)
 - The default port won't show up on a basic nmap scan, but other misleading ports will

6. Venusville
 - Non-standard port scan (high port) -- 2345

7. Last_Resort
 - Portscan without nmap -- use nc
 - http://www.g-loaded.eu/2006/11/06/netcat-a-couple-of-useful-examples/

8. Resistance_Base
 - Learn about stealth scans here! Figure out which types of scans work on which hosts!

9. Control_Room

Additional hosts:
 - Steath_Fin
 - Stealth_Null
 - Stealth_Xmas
The goal with these hosts is to see which stealth scans are blocked.
Idealy, these hosts should only be scannable from one host.
