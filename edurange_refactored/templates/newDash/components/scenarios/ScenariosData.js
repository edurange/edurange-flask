import elf from '../../../assets/img/card_img/elf.svg';
import fingerprint from '../../../assets/img/card_img/fingerprint.svg';
import getting_started_icon from '../../../assets/img/card_img/getting_started.svg';
import kick from '../../../assets/img/card_img/kick.svg';
import survivalist from '../../../assets/img/card_img/survivalist.svg';
import alchemy from '../../../assets/img/card_img/alchemy.svg';
import maze from '../../../assets/img/card_img/maze.svg';
import twoHeads from '../../../assets/img/card_img/twoHeads.svg';
import wrangler from '../../../assets/img/card_img/wrangler.svg';




export class ssh_Inception_shell {
    constructor(input = {}) {
        this.name = "ssh_Inception"
        this.keywords = ["ssh", "Linux shell"]
        this.icon = maze;
        this.description_short = "ssh_Inception teaches students the basics of ssh, a secure a program for logging into a remote machine.",
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class Total_Recon_shell {
    constructor(input = {}) {
        this.name = "Total_Recon"
        this.keywords = ["nmap", "directory traversal", "Linux shell"]
        this.icon = survivalist;
        this.description_short = "Total Recon is a progressive, story-based game designed to teach nmap network reconnaissance."
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class File_Wrangler_shell {
    constructor(input = {}) {
        this.name = "File_Wrangler"
        this.keywords = ["directory traversal","Linux shell"];
        this.icon = wrangler;
        this.description_short = "File Wrangler teaches the basics of files and directories in the Linux command line.",
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class ELF_Infection_shell {
    constructor(input = {}) {
        this.name = "ELF_Infection"
        this.keywords = ["Binary", "somethingElse"]
        this.icon = elf;
        this.description_short = "This game teaches about infected binaries. ",
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class strace_shell {
    constructor(input = {}) {
        this.name = "strace"
        this.keywords = ["Binary", "strace"]
        this.icon = fingerprint;
        this.description_short = "This game uses strace to examine executable files.",
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class Getting_Started_shell {
    constructor(input = {}) {
        this.name = "Getting_Started"
        this.keywords = ["Linux shell"]
        this.icon = getting_started_icon;
        this.description_short = "Getting Started teaches the basics of using the terminal on Linux (but also can extend to Mac).",
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class Metasploitable_shell {
    constructor(input = {}) {
        this.name = "Metasploitable"
        this.keywords = ["metasploit", "somethingElse"]
        this.icon = twoHeads;
        this.description_short = "This game teaches the basic usage of the metasploit framework.",
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class Web_Fu_shell {
    constructor(input = {}) {
        this.name = "Web_Fu!"
        this.keywords = ["Cross-site scripting (XSS)", "SQL injection (SQLi)"]
        this.icon = kick;
        this.description_short = "Web_Fu! teaches the basics of web application security. Put in practice your SQLi and XSS skills!",
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class Treasure_Hunt_shell {
    constructor(input = {}) {
        this.name = "Treasure_Hunt"
        this.keywords = ["pwn","Linux shell", "somethingElse"]
        this.icon = map;
        this.description_short = "Treasure Hunt is an exercise that teaches about permissions and other security loopholes in Linux. The goal is to find the passwords of 16 fake users.",
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class Ransomware_shell {
    constructor(input = {}) {
        this.name = "Ransomware"
        this.keywords = ["Web security","Ransomware", "somethingElse"]
        this.icon = alchemy;
        this.description_short = "Description needed for Ransomware",
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};