# Web Fu

## Learning objectives
1. Exploit vulnerable web pages using SQL injection
2. Retrieve information from other tables using the `UNION` operator
3. Bypass simple WAFs (Web Application Firewall)
4. Exploit vulnerable web pages using XSS (Cross-Site-Scripting)

## Connection Instructions

You can find the vulnerable webapp at port 8443 of the EDURange platform.

## Extra Resources
[OWASP SQLi Guide](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection.html)

[PortSwigger SQL Guide](https://portswigger.net/web-security/sql-injection)

## Exercises

### Level 1 (SQL-1.php)
The query being run on this page is:

`SELECT * FROM countries WHERE name='<ARG>';`

<question>
<question>
<question>

### Level 2 (SQL-2.php)
The query being run on this page is:

`SELECT * FROM books WHERE author LIKE '%<ARG>%';`

<question>
<question>
<question>

### Level 3 (SQL-3.php)

Hint: First find a way to count the number of columns in the table

<question>
<question>

### Level 4 (XSS-reflected-1.php)

[Hint](https://edurange.watzek.cloud:8443/XSS-reflected-1.php?parameter=value)

<question>

### Level 5 (XSS-reflected-2.php)

Look at the source.

<question>

### Level 6 (XSS-stored-1.php)

<question>

