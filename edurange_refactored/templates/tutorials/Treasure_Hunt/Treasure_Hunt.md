# Treasure Hunt

### Description

Treasure Hunt is an exercise that teaches about permissions and other security loopholes in
Linux. In this virtual machine there are 16 imaginary users. Somewhere in his/her home
directory, each of these imaginary users has a “secret” file named username-secret.<ext>
(where <ext> is a file extension) whose contents are intended to be private (readable only by
the user and no one else). However, each of their secret files can actually be read by other
users who are both determined and clever. 

Your goal is to collect the contents of as many of the
sixteen secret files as you can.

 ---

### Background
There are often multiple users on the same system or network. Given this case, how does a
system determine who is able to access specific files?

Linux system of file access permissions are used to control who is able to read, write and execute certain files. This is used both to keep
user files private as well as to protect critical system files. In order to obtain many of the secrets
in this exercise, you will need to understand the read, write, and execute permissions as well as
how permissions are applied to the owner, group owner, and every user. 

If you are unfamiliar with linux permissions, see the section on Linux File Permissions in the Student Tutorials
section below.

This exercise also utilizes password cracking for a few users. That password cracking method
that you will work with utilizes linux password hashes. This exercise is not intended to teach
about hashes and password security techniques. If you are unfamiliar with the general idea of
them, a quick web search should catch you up with the basics. 

The files that contain the password hashes are not publicly available on linux systems, but we have made them so for this
exercise and will show where to find them. Hopefully, this will give you an idea if the passwords
you use are secure or not!


You will also run into the .htaccess file in this exercise. This is a configuration file for Apache
Web Server. It is used for many things but here it is only used from user authorization. You
should be able to figure it out when you come across it. If not, a simple web search will help you
out again.

 --- 
### Learning Objectives
Know the difference between read, write, and execute permissions and how this affects
directories and files U

Understand linux groups

Understand what Set User ID and Set Group ID do

Know how to find a file’s permissions and interpret this and similar lines ‘-rwsr-xr-x‘

Be able to create a symbolic link and know what it does

Recognize what sorts of passwords are easily cracked from known password hashes

Have a moderate understanding of some basic linux tools and how to use them

### Instructions
Connect to the scenario via your instructor’s directions, or as displayed on the EDURange page.

Once logged in, it is your goal to find the secrets of the following 16 fake users:

* Alice Wan (awan)
* Bob Duomo (bduomo)
* Cathy Dry (cdry)
* Debbie Shi (dshi)
* Ellen Quintus (equintus)
* Fred Sexon (fsexon)
* George Hepta (ghepta)
*  Helen Ochoa (hochoa)
* Inna Nunez (inunez)
* Jack Dekka (jdekka)
* Karen Elva (kelva)
* Loretta Douzette (Idouzette)
* Patricia Kaideka (pkaideka)
* Pyotr Theodore Radessime (pradessime)
* Quinn Sanera (qsanera)
* Tudor Daforth (tdaforth)

---
#### Important Disclaimer:
Accessing some secret files will require that you make changes to certain files/directories in the
accounts of the fake users. Once you determine the secret, be sure to undo any changes that
you make so that you leave the system exactly in the same state that you found it. 

Otherwise, you could (1) make it very easy for others to access the information you worked so hard to get
or (2) make it impossible for others to access the information you found (this is unacceptable in
this exercise, though not in the real world).

Since some of your changes may be hard for you to undo, you can use the `resetFakeUsers`
command to resets all fake user accounts to their initial states and also resets other parts of the
system (e.g. deletes all files in the /tmp directory). 

Executing this command should solve all reseting issues; if it does not, please let us know. By calling resetFakeUsers frequently, you
could cause a denial of service attack against your classmates; please do not do this!
 ---
### User Secrets
Each secret is contained somewhere in that user's home directory. All fake users belong to a
group named student, a fact that is important for some of the attacks. There are other significant
groups as well that some of these users are in.

There is no strict sequential order for finding the secrets, though some you will only be able to
get after gaining access to another user's account. Password cracking is a great place to start.
We will walk you through that below.

--- 
### Password Cracking:

For password cracking download [John the Ripper](http:/Awww.openwall.com/john/) onto a
local computer. John the Ripper is not on the Treasure Hunt container, and you won't be able to install
it there. 

If you only have access to a Windows computer for your local machine, John the Ripper
suggests HashSuite; though we won't provide you with instructions on how to use that program.

On the Treasure Hunt mcontainer, gain access to the file /etc/shadow. (See hints below if stuck).
You will need a copy of /etc/shadow and /etc/passwd on your machine running John the Ripper.

Next, use John’s unshadow command to combine /etc/passwd and /etc/shadow into a single
password file (e.g. ‘'unshadow passwd shadow > mypasswd’).
Manually edit 'mypasswd' to exclude all accounts other than the 16 fake users for this problem —
otherwise you’re wasting processing time in your password cracker. 

When you find the secret of a fake user, removing that user from the unshadowed file will help speed up future attempts.
You do not want to waste processing time trying to crack passwords you don’t need!

Run John on 'mypasswd' (e.g. ‘john passwords’). The basic john command uses the default
wordlist run/password.Ist, which should be able to fairly quickly crack two user passwords.
There is one more password that can be cracked, but you will need to feed john a custom word
list. Maybe if you Knew more about fake users...


### User Web Pages:
Each user has at least one web page in a public html directory. Some of these pages contain
information relevant to finding their secret. Although many of the user web pages are publicly
readable by any user on the THVM, some can only be read via a web browser. 

Since you are logged in via ssh, you might be wondering how you can view these web pages. 
Lynx is a textbased web browser that we have provided for your use. Typing `lynx localhost/~awan/` will let
you view awan's homepage. The same format can be used to view the other 15 user's pages.

Though you can see the public html pages in each user's directory, due to the permissions of
any private files, you will need to use Lynx to uncover some of the secrets. See Lynx's man
page for specific instructions. 

`wget` and `curl` are also good alternative tools, since Lynx may not show you everything...

### Other Hints:
- It may be helpful to export certain files from the THVM to your local computer (or vice versa).
  You can use scp or ftp from your local computer to do this.
  
- Having trouble gaining access to /etc/shadow? Look in /bin/ and see if you can find something
  to help you.
  
- Access to web directories can be controlled by a .htaccess file. See
  http://www.javascriptkit.com/howto/htaccess.shtml for documentation on .htaccess files.
  
- The web server runs as user/group www-data. Including www-data in a group gives the web
  server whatever permissions are given to the group. There is a group named apache whose
  only member is www-data.
  
- In an HTML file, text between <!-- and > is a comment that is not displayed by the web
  browser.
  
- The utility `pdftotext` is installed for reading pdf files in the console. Alternatively, you may want to export relevant
  .pdf files from the THVM to your local computer and view them there.)
  
- It is possible to convert .pdf files to other file formats, and there are programs in the THVM for
  doing this. But saying exactly what those programs are would make one secret too easy too
  find. So you might want to research how to convert .pdf files to other formats in Linux.
  
- .docx format is a zipped (compressed) directory of XML files; it can be uncompressed with the
  unzip command. There are many ways to obtain that secret though.
  
- If you want to add a directory dir to the front of your PATH variable, a good way to do this is
  with the following command - export PATH= dir :$PATH (e.g. ‘export PATH=/tmp/:$PATH’)
  
- The strings command could be helpful for some secrets. As well as a hex viewer.
