# MemLabs Lab 1 WriteUp

## Overview - Beginner's Luck

My sister's computer crashed. We were very fortunate to recover this memory dump. Your job is get all her important files from the system. From what we remember, we suddenly saw a black window pop up with some thing being executed. When the crash happened, she was trying to draw something. Thats all we remember from the time of crash.

## Flag #1

In the description, we're told a black box popped up. Sounds like it could be a command prompt? Using consoles to see what commands were run, we can see a base64 encoded string. Let's decode it!

![Consoles](/images/memlab-lab1/f1.png)

![Base64 Decode](/images/memlab-lab1/f2.png)

## Flag #2
We also know Alissa was drawing at the time of the crash so I bet that is flag #2. Looking back at the process list, mspaint.exe was running. We'll use memdump to dump that process.

![Mspaint.exe](/images/memlab-lab1/f11.png)

![Memdump](/images/memlab-lab1/f12.png)

Since I expect this to be an image and not a text, xxd and strings won't help me here. However, a quick Google search brought me to this blog post: https://w00tsec.blogspot.com/2015/02/extracting-raw-pictures-from-memory.html

After downloading GIMP and scrolling for what seemed like eternity, I found the flag hidden in a sea of yellow.

![Gimp results](/images/memlab-lab1/f13.png)

## Flag #3
Finally, the third goal was to recover important files. We can use filescan to see what files were open. If you look, the username is "Alissa Simpson" so let's grep for that string. Scrolling through the results, we can find an "Important.rar" file.

![Grep filescan results](/images/memlab-lab1/f3.png)

![Important.rar file](/images/memlab-lab1/f4.png)

We can dump this file using dumpfiles command

![Dumpfiles](/images/memlab-lab1/f5.png)

When trying to run unrar, it appears to be password protected. To unlock, we need Alissa's NTLM hash in uppercase.

![Unrar needs password](/images/memlab-lab1/f6.png)

Off to dump hashes using hashdump!

![Hashdump](/images/memlab-lab1/f7.png)

To make it easy on ourselves, I'm going to run tr to transform the hash from lower to uppercase.

![Transform to upper](/images/memlab-lab1/f8.png)

Let's try running unrar again and give it the hash.

![Unrar success](/images/memlab-lab1/f9.png)

Woo hoo! It works! Opening up the image shows us this:

![Flag 3](/images/memlab-lab1/f10.png)
