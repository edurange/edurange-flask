while(1)
{
	system("cat /usr/local/src/logs/ttylog.\$\(hostname\).\$\(whoami\).* > /usr/local/src/logs/alltty.\$\(hostname\).\$\(whoami\)");
	system("python3 /usr/local/src/ttylog/analyze.py /usr/local/src/logs/alltty.\$\(hostname\).\$\(whoami\)" . " /usr/local/src/logs/\$\(whoami\)/.cli.csv");
	system("python3 /usr/local/src/ttylog/makeTsv.py /usr/local/src/logs/\$\(whoami\)/.cli.csv" . " /usr/local/src/logs/\$\(whoami\)/.cli.log");
	sleep(25);
}
