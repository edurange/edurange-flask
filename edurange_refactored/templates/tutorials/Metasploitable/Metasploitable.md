# Metasploitable

Work in Process

---
## What is Metasploit
Metasploit is a framework for automating the process of exploiting vulnerabilities in application software. It has tools to support the cyber kill chain. which consists of the steps: 
- reconnaissance, identifying the target and software services running on the target
- finding vulnerabilities, this may include CVEs for the specific software versions running on the target and severity of the vulnerabilities
- weaponization, identifying exploits that could be used for the vulnerabilities
- delivery, in order to get the exploit to the target, it may be necessary to bypass firewalls
- exploitation, choosing a payload, producing packets that contain the exploit with payload and delivering them to the target
- persistence, creating accounts, backdoors, beacons, etc. 

## Learning Objectives
- use the Metasploit shell.
- identify targets and services running on open ports
- given the service running and the version, find known vulnerabilities and severity.
- find exploits provided by the Metasploit framework to use.
- use the Metasploit Framework to exploit a vulnerable service.

<hr>
<h2 class="colH3"> Basic Metasploit Commands </h2>

Much like Bash, a Metasploit command is often followed by one or more input flags/values (we use square brackets to show when those are necessary). Enter the `msfconsole` command in the attacker machine to open a Metasploit shell, then try a couple of the following commands:

- `help`: when used alone, shows the possible options; when used with a command as input, shows information on the specified command.

- `search [search_term]`: searches the Metasploit vulnerability database and returns the available exploit module names.

- `use [module_name]`: tells Metasploit which exploit is being used.

- `back`: tells Metasploit to stop using the current exploit.

- `options`: shows the options that can be set for the exploit currently in use. (NOTE: some options are required for the exploit to be run.)

- `set [option] [value]`: sets the given option to the given value for the exploit currently in use.

- `exploit`: tells Metasploit to try to run the current exploit.

- `exit`: can be used to exit the Metasploit command line and return to the bash shell (`quit` can be used for the same purpose).

> Note: options such as RHOSTS which holds information for the target ip address will likely have to be set for each exploit used.

### Example use of Metasploit

The following is an example use of the metasploit framework that has been generalized to show how the given commands can be used.

![Metasploit Command Line Example](/static/build/img/Metasploitable/m-h_example_cmd_line.png)
<pre>
msf > use windows/smb/ms08_067_netapi
exploit(ms08_067_netapi) > show options
exploit(ms08_067_netapi) > set RHOST 10.0.0.1
exploit(ms08_067_netapi) > show targets
exploit(ms08_067_netapi) > set target 0


</pre>

---

## Services

The following is a list of the types of vulnerable services provided by Metasploitable

- A compiler

- An internet relay chat (irc)

- Two file transfer protocols (ftp)

- An http service (php_cgi)

- An sql database

---

## Information

Once you have logged into the attacker machine, you should be able to run nmap, which is the standard tool for scanning a target. The use of nmap
is covered in the scenarios SSH_inception and Total Recon. In this exercise, the target machine can be accessed using the keyword `target` instead of scanning a network to find the IP Address.

It is recommended that when you scan the target machine, to scan all ports from 0 to 65535. Once you have identified the open ports you can narrow down the range of ports that you scan for additional information.

When you scan the target machine you should see 15 open ports.

The next step is to identify services with known vulnerabilites.

When looking for exploits to use on a service, we highly recommend that you only try exploits that are ranked `excellent`.

---
