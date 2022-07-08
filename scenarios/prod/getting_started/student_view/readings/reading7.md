
Not all files appear as they really are. Just because you see a file that says, `imanimage.png` does not mean that it is an image. It could be a text file or a harmful file if executed! So... how do you protect yourself? One way is with the file command!

### file

To find out what a file really is regardless of its extension is file. Check out the man page. Give it a peruse by typing in man file. What type of options are there with file? Now let's test it. Type `q` to get out of the man page.

There are 2 files in your Linux box in a folder at your home directory called `/toLearn` . One is called `cat.jpg` and the other is `dog.jpg`

Both look like images to me! But if you type in `ls -l` you will notice that one is a lot larger in size than the other. One is about 25,000 bytes whereas the other is only about 20. Now let's see what is really going on.

Type

- `file dog.jpg`

You'll see something like, dog.jpg: ASCII text

Now type

- `file cat.jpg`

You'll see something like, cat.jpg: JPEG image data, Exif standard: TIFF image data, ... etc.

### cat

Now let's learn a new command, cat. cat prints out the text from a file.

Type

- `cat dog.jpg`
Go throu
You should see something like:

`meow I am a doggo`

TASK: In your home directory there is a folder called `stuff`. Open that up and find out what file types are in there. One is a text file (ASCII). `cat` that and find the secret code inside.

---

