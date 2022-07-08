
### Hierarchy

Linux folders and files are arranged like an upside down tree, where the slash `/` is called the root node, or beginning, of all your files in the entire computer. The root is the base of the tree and as you go down it keeps splitting into branches and leaves. The leaves would be a file and the branches are folders. This means that if you want to search the entire file system, you need to start at `/`

### `/` vs. logging in as root

The root, signified by a `/` , is the beginning of your files. But you can also log in as the root user. When you do this, your home directory (where your files are typically saved) is in the folder `/root` not at, `/`. The `/root` folder is not to be confused with the slash (root) the beginning of all the files. Just like if you were logged in as student you would typically save your files in `/home/student`, whereas the root user saves their files in `/root`.

### Important

A root user is someone who has access to everything on the computer. They could even delete everything in a computer. It is best practices to disable root or use a VERY strong password. For example using numbers, letters, capitals, special symbols and a random sampling of each, and no dictionary words.

---

<h2 class="colH3"> 4. Commands </h2>

What is a command? Commands are executable programs that you can call from your command-line terminal. The most common place to look for bash commands is in the `/bin` folder. Let's get started right away and use two different commands.

### cd

`cd` stands for "change directory", meaning to navigate to a new folder.
Type each of the following. One at a time. Hitting enter after each

- `cd /`
- `cd /root`
- `cd`
- `cd ../`

The first command sends you to the root of your entire file system.

The second command sends you to the user root folder, but notice that you don't have permissions to that directory.

The third command sends you to your home directory

The fourth sends you backwards (up) a level.

TASK: `cd` to `/bin` then `cd` back to your home directory.

### ls

`ls` "lists" the files and directories of where you are now.

Type

- `ls`

