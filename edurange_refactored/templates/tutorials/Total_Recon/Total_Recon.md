# Total Recon

---

## 1. About

Total Recon is a story-based game designed to teach how network
protocols such as TCP, UDP, and ICMP can be used to reveal information about
a network. Total Recon focuses on reconnaissance to determine hosts in an
unknown network. You will explore tradeoffs between speed and stealth when
using tools such as nmap.

---

## 2. Background

Whether you're doing a large-scale security audit, inventorying a network, or
analyzing network response times, nmap is a powerful tool to help you complete
your task. In order to understand this exercise, you should be familiar with the
3-way handshake for TCP. A basic understanding of ICMP and UDP will also
be helpful. This exercise is not designed to teach you all of the details of those
protocols, but rather to show you how they can be used for network exploring.
You will learn how to discover hosts on a network, determine which ports on
those hosts are open, and what applications are running on them.
In practice, each message that is sent over the Internet uses multiple protocols,
which are divided into five layers: physical layer, link layer, network layer,
transport layer and application layer. For example, the physical layer handles
what is encoded as a 0 or 1. The link layer handles communication on local area
networks (LANs). The network layer handles routing on wide area networks
(WANs), e.g. IP. The transport layer handles ports and processes, e.g. TCP,
UDP, ICMP. The application layer handles applications communicating with
each other, e.g. http, ftp, by nesting packets inside of packets. In general, these
packets correspond to layers of functionality: TCP is connection-oriented and is
responsible for a number of things including reliably conveying messages between
the application layers on two hosts. The three-way handshake establishes this
pairing with the following sequence: SYN, SYN-ACK, and ACK You can get a
summary of the important protocols and their layers in: Chapter 4 of Hacking:
The Art of Exploitation (Erickson)[1] or Chapter 2 of Counter Hack Reloaded
[2]. Network Security by Kaufman, Perlman, Speciner [3].

---

## 3. Learning Objectives

Understand how the networking protocols (TCP, UDP, ICMP) can be
exploited for recon

- Know how to use nmap to find hosts and open ports on a network

- Recognize the standard common ports (e.g. SSH, FTP, HTTP, SMTP,
IMAP)

- Understand the TCP flags and how they can be used for different types of
scans

- Understand CIDR network configuration and how to subdivide a network
IP range

---

## 4. Instructions

Connect to the VM via your instructor's directions, or as displayed on your
EDURange account. Instructions will be displayed upon logging in and at each
new checkpoint.

---

## 5. Lab Assignments and Questions

Questions can be found upon logging into your EDURange account.

---

## 6. Discussion Questions

1. What is the 3-way handshake?

2. What does 10.1.1.0/17 mean? how many IP addresses does that include?

3. What does the SYN flag do? What does the FIN flag do?

4. What are the options for nmap and what are their differences in terms of
time, stealth and protocols?

5. Which methods did you use to speed up your scans? What else could you
have done?

---