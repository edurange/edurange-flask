README for strace files
Lyn Turbak, 2016/03/13

Files in the directory:

copy.c
empty.c
hello.c /* this is new */
mystery.c
README
script.sh
strace-identify
tiger.txt
trojaned_cat.c /* this is modified */

Directions: 

1. Copy copy.c, empty.c, hello.c, script.sh, strace-identify, and tiger.txt to a directory that everyone can read

2. Compile mystery.c to an executable named "mystery" and move it to the same directory as in Step 1. Delete mystery.c so students can't find it. 

3. Compile trojaned_cat.c to an executable named "cat" and move it to a directory in PATH that comes before /bin (where the "real" /bin/cat lives). Delete trojaned_cat.c so that students can't find it. 

4. Create a directory /tmp/data with permissions 733 with owner and group root. This is the directory in which each file displayed by cat will be squirreled away in a separately named file. Naming each file separately (rather than appending all displayed files in one big file) avoids the doubling explosion of the previous version. 

The 733 permissions make it impossible to "stumble upon" the files stored in /tmp/data. However, files in /tmp/data whose names are known can be read by all. By using strace, it is possible to see that there's a list of all squirreled-away files in /tmp/data/filenames, and people can work from there. 



