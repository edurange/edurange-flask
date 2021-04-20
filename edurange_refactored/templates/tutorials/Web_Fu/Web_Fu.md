# Web Fu

## Connection Instructions:

You can find the vulnerable databases at port 8443 of the EDURange platform

## Reading/Extra Resources:
[OWASP SQLi Guide](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection.html)

[PortSwigger SQL Guide](https://portswigger.net/web-security/sql-injection)


## Level 1 (1.PHP)
The query being run on this page is:

`SELECT * FROM countries WHERE name='<ARG>';`
## Level 2 (2.PHP)
The query being run on this page is:

`SELECT * FROM books WHERE author LIKE '%<ARG>%';`

## Level 3 (3.PHP)

Hint: First find a way to count the number of columns in the table



---
