
import elf from '../../../../../assets/img/card_img/elf.svg';
import fingerprint from '../../../../../assets/img/card_img/fingerprint.svg';
import gettingStarted from '../../../../../assets/img/card_img/getting_started.svg';

import kick from '../../../../../assets/img/card_img/kick.svg';
import survivalist from '../../../../../assets/img/card_img/survivalist.svg';
import alchemy from '../../../../../assets/img/card_img/alchemy.svg';
import maze from '../../../../../assets/img/card_img/maze.svg';
import twoHeads from '../../../../../assets/img/card_img/twoHeads.svg';
import wrangler from '../../../../../assets/img/card_img/wrangler.svg';
import treasureMap from '../../../../../assets/img/card_img/tmap.svg';
import React from 'react';

export class UserScenarioShell {
    constructor(input = {}) {
        this.id = input.scenario_id ?? 'none';
        this.uid = input.uid ?? 'none';
        this.name = input.scenario_name ?? 'none';
        this.description = input.scenario_description ?? 'none';
        this.ownerID = input.scenario_owner_id ?? 'none';
        this.status = input.scenario_status ?? 'none';
        this.created_at = formatDate(input.scenario_created_at) ?? 'none';

        this.guidePages = [ ]
        this.complete = input.complete || false;
    };
}

export class UserFullShell {
    constructor(input = {}) {
        this.id = input.id ?? 'none';
        this.uid = nanoid(5);
        this.username = input.username ?? 'none';
        this.role = (input.username) ? assignUserRole(input) : 'none'; // assigns role if user exists, otherwise 'none'
        this.is_active = input.is_active || true; // just add both to avoid bugs
        this.active = input.active || true; // the db is weird about these props, leave them alone :)
        this.email = input.email ?? 'none';
        this.scenarios = { }
        this.userGroups_memberOf = input.userGroups_memberOf ?? [];
        this.scenarios_memberOf = input.scenarios_memberOf ?? [];
        this.created_at = formatDate(input.created_at) ?? 'none';
    };
};


// these classes are called by their .name from /dashboard/scenarios/ in this format:
// ScenariosData.shells[`${theScenarioName}`] }

// the 'shells' object at the end of the file maps to the actual 'shell' objects.

// in other words: if you change the names of these classes, you will need to update
// any scripts that might call them.

// likewise, if the 'name' property is changed in session_instructordata_state.scenarios,
// then this script will need to be updated as well.
export class Getting_Started_shell {
    constructor(input = {}) {
        this.keywords = ["Linux shell"]
        this.icon = gettingStarted;
        this.description_short = '"Getting Started" teaches basics of the Linux terminal shell.  These skills may also extend to the Mac terminal.',
        this.description_long = (
            <>
                {/* <article className='dashcard-fullview-guide-main-text'> */}
              <br></br>
              Welcome to "Getting_Started"!
              <br></br>
              <br></br>
              This window will be both your guide and your judge.⚖️
              <br></br>
              <br></br>
              You can move to a guide page by clicking its tab at the top of this viewport.
              <br></br>
              <br></br>
              To play Getting_Started, connect with SSH!  SSH connection information and connection buttons are on the bottom of this guide viewport.
              You can either connect with your own terminal (recommended), or use the 'Web-SSH' option to launch an in-browser SSH connection.
              <br></br>
              <br></br>
              Each challenge in the SSH game is paired with a question in this window, so when you find a secret answer or flag,
              come back to this window, and enter your answer into the provided field.  If you got the right answer, you will be awarded points!
              <br></br>
              <br></br>
              If you're having trouble, check out some of the challenge-specific resources to the left of this guide or our FAQ(link).
              If you're still having trouble, try the chat!
              <br></br>
              <br></br>
              Good luck, and have fun!
              <br></br>
              <br></br>
            {/* </article> */}
            </>
        )
        ;
    };
};

export class Ssh_Inception_shell {
    constructor(input = {}) {
        this.keywords = ["ssh", "Linux shell"]
        this.icon = maze;
        this.description_short = '"SSH_Inception" teaches basics of the "Secure Shell" (SSH), a secure protocol for logging into a remote machine.',
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class Total_Recon_shell {
    constructor(input = {}) {
        this.keywords = ["nmap", "directory traversal", "Linux shell"]
        this.icon = survivalist;
        this.description_short = '"Total_Recon" is a progressive, story-based game designed to teach nmap network reconnaissance.'
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class File_Wrangler_shell {
    constructor(input = {}) {
        this.keywords = ["directory traversal","Linux shell"];
        this.icon = wrangler;
        this.description_short = '"File_Wrangler" teaches the basics of files and directories in the Linux command line.',
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class ELF_Infection_shell {
    constructor(input = {}) {
        this.keywords = ["Binary", "somethingElse"]
        this.icon = elf;
        this.description_short = "This game teaches about infected ELF binaries.",
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class Strace_shell {
    constructor(input = {}) {
        this.keywords = ["Binary", "strace"]
        this.icon = fingerprint;
        this.description_short = '"Strace" is a game that teaches how to use Linux `strace` to examine executable files.',
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};

export class Metasploitable_shell {
    constructor(input = {}) {
        this.keywords = ["metasploit", "somethingElse"]
        this.icon = twoHeads;
        this.description_short = `"Metasploitable" is a game that teaches the basic usage of the Metasploit framework.`,
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class Web_Fu_shell {
    constructor(input = {}) {
        this.keywords = ["Cross-site scripting (XSS)", "SQL injection (SQLi)"]
        this.icon = kick;
        this.description_short = `"Web_Fu" teaches the basics of web application security. Put in practice your SQLi and XSS skills!`,
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class Treasure_Hunt_shell {
    constructor(input = {}) {
        this.keywords = ["pwn","Linux shell", "somethingElse"]
        this.icon = treasureMap;
        this.description_short = `"Treasure_Hunt" is an exercise that teaches about permissions and other security loopholes in Linux. The goal is to find the passwords of 16 fake users.`,
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};
export class Ransomware_shell {
    constructor(input = {}) {
        this.keywords = ["Web security","Ransomware", "somethingElse"]
        this.icon = alchemy;
        this.description_short = "blurb needed for Ransomware",
        this.description_long = "this is where the longer description for SSH_inception goes";
    };
};


export const scenarioShells = {

    Getting_Started: new Getting_Started_shell,
    Total_Recon: new Total_Recon_shell,
    File_Wrangler: new File_Wrangler_shell,
    Elf_Infection: new ELF_Infection_shell,
    Strace: new Strace_shell,
    Metasploitable: new Metasploitable_shell,
    Ransomware: new Ransomware_shell,
    Treasure_Hunt: new Treasure_Hunt_shell,
    Ssh_Inception: new Ssh_Inception_shell,


}