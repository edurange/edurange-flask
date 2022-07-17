There are parameters and options you can give a command. What if you wanted to list the permissions of a file and find hidden files? (Yes there are hidden files!)

Now type

- `ls -la`

Then hit enter.

That's a lot of info! What you see is all the files and folders in the folder you are at currently.

- The first column is the type of file followed by permissions. `–` means a regular file. `d` is a directory (folder). `l` is a link. `rwx` are the permission for each file. `rwx` stands for `7` so `rwxrwxrwx` would be `777`. These correspond to binary. There are 3 bits. `000` would stand for `0`. `111` is `7`. `101` is `5`, etc. Each file has visible 3 permissions User, Group, Anyone.

- The next column is the number of links or directories in the folder

- The 3rd column is the user that owns the folder/file

- The 4th column is the group that owns the folder/file

- The 5th is the size of the file/folder

- The 6th is the month day and time it was last edited/touched

- And finally the file name




### Man Pages

Man Pages is short for manual pages. These are text documents with lots of information on commands. Remember the command we did for listing our files? `ls`! Let's find that man page.

Type

- `man ls`

and hit enter.

Remember we typed `ls -la`? Let's learn what `-l` and `-a` is!



#### -l

To search inside a man page, you use a `/` . Now type `/-l` and hit enter. You will probably see the page move to the first occurrence found and on top of that you should see that `-l` was highlighted. To move around your search keep hitting `n` (stands for next) until you see `-l` highlighted to the left. This will be above `-L` Long listing stands for listing the items in a row as seen in figure 2

#### -a

Type `/-a` and hit enter. Hit `n` till you can't go any further. Now hit `b` (stands for back) until you find the entry for `-a` which is above `-A`. The man page is telling you that files that start with `.` like `.bashrc` (which are typically hidden) are now going to be displayed.

#### q

When in a man page and you need to get out, just type `q`

TASK: Open the man page for `mv`. Can you give a brief description of what the command `mv` does?

- If you don't see it highlighted, you may have typed something by mistake or your console colors may not be optimized. If you typed something by mistake, just retype `/-l` etc.

