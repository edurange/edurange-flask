### Case Sensitivity

Case sensitivity means that HoW yoU labEL yoUR files matters. If you search for a file called hiya.docx, it would not be the same as finding a file, hiyA.docX.

### touch

`touch` is a command that ‘touches' a file. If the file exists it updates its modified date. If the file does not exist, then the file will be created with nothing in it. `man touch` to learn more.

### echo

`echo` will copy what you write to stdout (standard out, explained more later). You can use this in many different ways.

Type

- `echo "This is echoed"`

You will see that it was repeated back to you!

### Angle Brackets

Angle Brackets are `>` `>>` `<` `<<` . They have many uses. `>` Will replace a file with what you input. If the file already existed `>` will delete everything in that file and replace it with what you sent it. In contrast if you use `>>` , this will append what you sent to the bottom of the file, leaving the rest of the file intact. Let's give it a try.

Type

- `echo "This is cool" > newfile`

- `cat newfile`

Now type

- `echo "This is cool too" > newfile`

- `cat newfile`

You can see that `>` will replace any text with what you send it. While `>>` will append to a file

Type

- `echo "This is another thing" >> secondfile`

- `echo "Hello World" >> secondfile`

- `cat secondfile`

Now let's combine the two files.

Type

- `cat newfile >> secondfile`

- `cat secondfile`

You can see the newfile appended to the end of secondfile whereas if you cat newfile it will still only have what we added to it earlier.

TASK: There is a folder in your home directory called `textfiles`. There are three files, append them all to a new file called, `alltogether.txt` in your personal directory. (Your home directory)

The tip below is NOT required but only if you want a harder task!

There are many ways to accomplish this in one line, here is a hint for one way, type

`echo "one"; echo "two"; echo "three";`

One of the most useful tricks you can use angle brackets for is suppressing error messages. If you want to suppress all errors that may result from a command, add '2>/dev/null' to the end of your command. Ex: "find . filename 2>/dev/null". To learn more about what the number 2 stands for there, and what /dev/null is, read this reference on tty streams: <link TODO>


