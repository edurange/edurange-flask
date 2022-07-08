
### mv

`mv` is used to move a file from one location to another, or to rename a file. type `man mv`
to learn more.

### cp

`cp` is used to copy a file to a new location. Type `man cp` to learn more.

### less

less is more. The command less is used to open larger files, page by page. It allows you more tools to read a file in an organized fashion.

### cowsay

cowsay is probably one of the best commands... ever. Well maybe not ever, but it is fun!

- `cowsay "this is fun"`

### fortune

fortune gives you, well, a fortune! Go ahead give it a whirl!

### Piping

Piping is a new concept but stick with me on this one. When you give input to a command it is considered a standard in (STDIN). In other words it is data that is fed to a program/command. Whereas when you see something printed out back to you it is using standard out (STDOUT). A pipe, also recognized as `|` is used when you want something that is a STDOUT to then be used as the STDIN. To understand this we will use a fun example.

Remember fortune? If we just type fortune we get a fortune back. That fortune we get back is a STDOUT. But when we use cowsay we type something for the cow to say, which is STDIN. So we can use a pipe to take our fortune and have the cow say it!

- `fortune | cowsay`

### More vim

There are a few more really useful commands I would like to teach you about vim.

If you want to open up multiple files at the same time you can do:

- `vim fileone filetwo.c filethree.h filefour.cc`

Or you can open up another file or create a new file while you are still in vim with:

- `:e anotherfile.js`

And you can jump from file to file with the `:b` keystrokes and using tab to go through which file you would like to edit next.

---

