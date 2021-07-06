# Metasploitable

Work in Process

---

## Learning Objectives

- Learn to identify which services running on open ports are exploitable vulnerabilities.

- Learn which exploits provided by the Metasploit framework to use.

- Learn to use the Metasploit Framework to exploit a vulnerable service.

---

<h2 class="colH3"> Basic Metasploit Commands </h2>

> Square brackets indicate the command input.

- `msfconsole`: opens the Metasploit shell, which allows for Metasploit commands to be run.

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

Once you have logged into the attacker machine, the target machine can be accessed using the keyword `target` instead of using an IP Address.

It is recommended that when you scan the target machine, to scan all ports from 0 to 65535. Once you have identified the open ports you can narrow down the range of ports that you scan.

When you scan the target machine you should see 15 open ports.

When looking for exploits to use on a service, we highly recommend that you only try exploits that are ranked `excellent`.

---
