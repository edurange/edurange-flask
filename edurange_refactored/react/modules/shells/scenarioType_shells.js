
// FILE IN USE; KEEP

import elf from '../../assets/img/svg/small/elf.svg';
import fingerprint from '../../assets/img/svg/small/fingerprint.svg';
import gettingStarted from '../../assets/img/svg/small/getting_started.svg';

import kick from '../../assets/img/svg/small/kick.svg';
import survivalist from '../../assets/img/svg/small/survivalist.svg';
import alchemy from '../../assets/img/svg/small/alchemy.svg';
import maze from '../../assets/img/svg/small/maze.svg';
import twoHeads from '../../assets/img/svg/small/twoHeads.svg';
import wrangler from '../../assets/img/svg/small/wrangler.svg';
import treasureMap from '../../assets/img/svg/small/tmap.svg';
import resData from '../../pages/home/dashboard/scenarios/src/modules/scenarioResources';

// these classes are called by their .name from /dashboard/scenarios/ in this format:
// ScenariosData.scenarioShells[`${theScenarioName}`] }

// the 'scenarioShells' object at the end of the file maps to the actual 'shell' objects.

// in other words: if you change the names of these classes, you will need to update
// any scripts that might call them.

class Getting_Started_shell {
    constructor(input = {}) {
        this.keywords = ["Linux shell"];
        this.icon = gettingStarted;
        this.description_short = '"Getting Started" teaches basics of the Linux terminal shell.  These skills may also extend to the Mac terminal.';
        this.description_long = ("this is where the longer description goes");
        this.resources = [ resData.man, resData.ssh, resData.ls, resData.file, resData.echo, resData.touch, resData.angle_brackets, resData.vim, resData.find ]
    };
};
class Ssh_Inception_shell {
    constructor(input = {}) {
        this.keywords = ["ssh", "Linux shell"];
        this.icon = maze;
        this.description_short = '"SSH_Inception" teaches basics of the "Secure Shell" (SSH), a secure protocol for logging into a remote machine.';
        this.description_long = "this is where the longer description goes";
        this.resources = [ resData.man, resData.ssh, resData.grep, resData.locate, resData.find, resData.ftp ];
    };
};
class Total_Recon_shell {
    constructor(input = {}) {
        this.keywords = ["nmap", "directory traversal", "Linux shell"];
        this.icon = survivalist;
        this.description_short = '"Total_Recon" is a progressive, story-based game designed to teach nmap network reconnaissance.';
        this.description_long = "this is where the longer description goes";
        this.resources = [ resData.man, resData.ssh, resData.tcp, resData.udp, resData.icmp, resData.ftp, resData.smtp, resData.imap ];
    };
};
class File_Wrangler_shell {
    constructor(input = {}) {
        this.keywords = ["directory traversal","Linux shell"];
        this.icon = wrangler;
        this.description_short = '"File_Wrangler" teaches the basics of files and directories in the Linux command line.';
        this.description_long = "this is where the longer description goes";
        this.resources = [ resData.man, resData.ssh, resData.ls ];
    };
};
class ELF_Infection_shell {
    constructor(input = {}) {
        this.keywords = ["Binary"];
        this.icon = elf;
        this.description_short = "This game teaches about infected ELF binaries.";
        this.description_long = "this is where the longer description goes";
        this.resources = [ resData.man, resData.ssh, resData.elf ];
    };
};
class Strace_shell {
    constructor(input = {}) {
        this.keywords = ["Binary", "strace"];
        this.icon = fingerprint;
        this.description_short = '"Strace" is a game that teaches how to use Linux `strace` to examine executable files.';
        this.description_long = "this is where the longer description goes";
        this.resources = [ resData.man, resData.ssh, resData.strace ];
    };
};

class Metasploitable_shell {
    constructor(input = {}) {
        this.keywords = ["metasploit"];
        this.icon = twoHeads;
        this.description_short = `"Metasploitable" is a game that teaches the basic usage of the Metasploit framework.`;
        this.description_long = "this is where the longer description goes";
        this.resources = [ resData.man, resData.ssh, resData.metasploit ];
    };
};
class Web_Fu_shell {
    constructor(input = {}) {
        this.keywords = ["Cross-site scripting (XSS)", "SQL injection (SQLi)"];
        this.icon = kick;
        this.description_short = `"Web_Fu" teaches the basics of web application security. Put in practice your SQLi and XSS skills!`;
        this.description_long = "this is where the longer description goes";
        this.resources = [ resData.man, resData.ssh ];
    };
};
class Treasure_Hunt_shell {
    constructor(input = {}) {
        this.keywords = ["pwn","Linux shell"];
        this.icon = treasureMap;
        this.description_short = `"Treasure_Hunt" is an exercise that teaches about permissions and other security loopholes in Linux. The goal is to find the passwords of 16 fake users.`;
        this.description_long = "this is where the longer description goes";
        this.resources = [ resData.man, resData.ssh ];
    };
};
class Ransomware_shell {
    constructor(input = {}) {
        this.keywords = ["Web security","Ransomware"];
        this.icon = alchemy;
        this.description_short = "blurb needed for Ransomware",
        this.description_long = "this is where the longer description goes";
        this.resources = [ resData.man, resData.ssh ];
    };
};

export const scenarioShells = {

    Getting_Started:    new Getting_Started_shell,
    Total_Recon:        new Total_Recon_shell,
    File_Wrangler:      new File_Wrangler_shell,
    Elf_Infection:      new ELF_Infection_shell,
    Strace:             new Strace_shell,
    Metasploitable:     new Metasploitable_shell,
    Ransomware:         new Ransomware_shell,
    Treasure_Hunt:      new Treasure_Hunt_shell,
    Ssh_Inception:      new Ssh_Inception_shell,

};