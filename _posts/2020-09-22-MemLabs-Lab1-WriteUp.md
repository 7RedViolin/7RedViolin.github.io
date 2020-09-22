## MemLabs Lab 1 WriteUp

### Overview - Beginner's Luck

My sister's computer crashed. We were very fortunate to recover this memory dump. Your job is get all her important files from the system. From what we remember, we suddenly saw a black window pop up with some thing being executed. When the crash happened, she was trying to draw something. Thats all we remember from the time of crash.

### Flag #1

In the description, we're told a black box popped up. Sounds like it could be a command prompt? Using consoles to see what commands were run, we can see a base64 encoded string. Let's decode it!

### Flag #2
We also know Alissa was drawing at the time of the crash so I bet that is flag #2. Looking back at the process list, mspaint.exe was running. We'll use memdump to dump that process.

Since I expect this to be an image and not a text, xxd and strings won't help me here. However, a quick Google search brought me to this blog post: https://w00tsec.blogspot.com/2015/02/extracting-raw-pictures-from-memory.html

After downloading GIMP and scrolling for what seemed like eternity, I found the flag hidden in a sea of yellow. That looks a lot like the string flag{g00d_BoY_good_girL}.

### Flag #3
Finally, the third goal was to recover important files. Let's use filescan to see what files were open.

I notice the username is "Alissa Simpson" so let's grep for that string. Scrolling through the results, we can find an "Important.rar" file.

We can dump this file using dumpfiles command

Off to dump hashes using hashdump!

To make it easy on ourselves, I'm going to run tr to transform the hash from lower to uppercase.

Let's try running unrar again and give it the hash.

Woo hoo! It works! Opening up the image shows us this:
