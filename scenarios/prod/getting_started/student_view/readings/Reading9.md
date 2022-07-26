### vim

vim is a program that is used to edit files, and will hopefully be your new best friend! There are different editors out there for example, nano and emacs. To create a file just type

- `vim mynewfile.txt`

Or

- `vim thisisfun`

To edit a file that is already created it's the same procedure, just make sure not to misspell it or you'll create a new file with that spelling.

Once you are in vim the main key strokes to editing a file are:

- `i` - This puts you in edit mode to type and delete text like you normally would

- `esc` - Hitting the escape key will take you out of edit mode. `:w` - These keystrokes will save the file. `w` stands for write. `:q!` - To quit without saving. Did you edit a file and don't want to commit that change? These keystrokes will exit vim and NOT save your file.

- `:q` - These keystrokes will quit the vim program. You can also do `:wq` to save the file and quit right away. `:q` will not work unless you have saved your file or you have made no changes what-so-ever.

`dd` - When you are NOT in edit mode this will delete an entire line. (Make sure your cursor is on the line you want to delete).

`u` - If you make changes that you didn't mean to, you can press `u` for 'undo' - And if you undo too many things you can press Ctrl+R to 'redo'

`0` - zero will take you to the beginning of a line

`$` - will take you to the end of a line

There is a LOT that vim can do but we won't list it all here. Do a search on the internet to learn more! You can also check out a vim command cheat sheet, here and here. But at the end of this lesson will be a couple more commands that you will find to be amazingly helpful! You can also check out vimtutor:

- `vimtutor`

TASK: In your home directory in a folder called `editme` there is a file called `editme.txt`, open that up in vim. Delete lines 4 and 5 and add 2 more lines of anything you would like at the end of the file. Don't forget to save.

### Regular Expressions

Regular expressions are used to help you find something on your computer and can be used in programming to enhance your programs. There are a LOT of websites out there that teach you all about it but the gist is that you can use symbols like a `*` to mean something when parsing through text. For example the `*` is a wild card. Let's say I wanted to find a file with the word spekter in it. But there could be other text before and after the word spekter. So I could say search for, spekter. This means, search for spekter and I don't care if there is anything else before or after.

To learn about how powerful regular expressions are check out these sites:

[regular expressions 1](https://regexone.com)

[regular expressions 2](https://regexr.com)

### find

This leads us to find. find is a very helpful tool that you can use to find things on your computer. Take a moment to peruse the man page for find. (man find) Get an idea of how it is used.

An example as given earlier:

- `find . -type f -iname *spekter*`

- What you see is the command find. The next `.` is telling us where we want to find. It's the path. The dot means, search in this location where I am at. We could also type in `/Documents` or a full path from the root. Where ever you need to search.

- The parameter `-type` is telling find that you specifically want to find a type of object, in this case, `f` stands for a regular file.

- `-iname` is telling the name of the file we are looking for. You can also use `-name` but `-iname` is case insensitive. This means that my search will pull up, SpeKter as well.

- Lastly, the `*`'s on either side again tell find that I want everything with spekter in it, regardless of what is around it. If I did not add that, my find will pull up nothing.

TASK: Hidden throughout your home directory are image files with the name, `edurange`. Take your skills and find all 6. Create a new file in your home directory and put the location and type of each in that file. Remember there are many types of file images. Png, jpg, jpeg, and gif to name the widely used ones.


