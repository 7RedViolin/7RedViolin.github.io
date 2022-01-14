---
layout: page
title: "KringleCon 4: Four Calling Birds WriteUp - Shellcode Primer"
date: 2022-01-13 21:00:00 -0500
tags: ctf kringlecon-2021 shellcode assembly
intro: How to read and write the contents of a file via shellcode
---

## Objective: Shellcode Primer
> Complete the Shellcode Primer in Jack's office. According to the last challenge, what is the secret to KringleCon success? "All of our speakers and organizers, providing the gift of ____, free to the community.

As a side note, I'm skipping through to the last challenge of the Shellcode Primer puzzle since they all build upon each other and the final question is like the capstone.

![Puzzle description](/images/kringlecon2021/shellcode_primer_1.png)

I'll break this down into five steps:

1. Get a references to the target file
```
call temp
db '/var/northpolesecrets.txt',0
temp:
pop rax
```
Here, we are storing the path to the target file in our register `rax` for future use.

2. Open the file via sys_open
```
mov rdi, rax
mov rax, 2
mov rsi, 0
syscall
```
For the sys_open syscall, we have to define the following registers:
- `rdi` = the filename (previously stored in `rax`)
- `rax` = now the integer that corresponds to our target syscall (in this case, sys_open)
- `rsi` = what mode we want to use when opening this file (e.g. read-only)

The file descriptor is then stored in `rax`.

3. Read the file via sys_read
```
mov rdi, rax
mov rax, 0
mov rsi, rsp
mov rdx, 500
syscall
```
For the sys_read syscall, we have to define the following registers:
- `rdi` = the file descriptor (previously stored in `rax`)
- `rax` = now the integer that corresponds to our target syscall
- `rsi` = the target address where we want to store what was read
- `rdx` = the number of characters to read (I wasn't sure how much data was in the file so I chose a decently large number)

In this instance, the register of importance is `rsp` since that saves the location where we stored what was read.

4. Output the contents to stdout via sys_write
```
mov rax, 1
mov rsi, rsp
mov rdx, 500
mov rdi, 1
syscall
```
For the sys_write syscall, we have to define the following registers:
- `rax` is the integer that corresponds to our target syscall
- `rsi` is the location where we stored what was read
- `rdx` is the number of characters we want printed (I made this the same amount as `rdx` used in the call to sys_read to make sure all data that was read was also written.)
- `rdi` is the file descriptor

5.   Exit the program via sys_exit
```
mov rax, 60
mov rdi, 1
syscall
```
For the sys_exit syscall, we have to define the following registers:
- `rax` is the integer that corresponds to our target syscall
- `rdi` is the exit code we want to pass

From there, we are ready to execute and find the flag!

![Results](/images/kringlecon2021/shellcode_primer_2.png)

To see my other writeups for this CTF, check out the tag [#kringlecon-2021](/tags#kringlecon-2021).

## References
- [Assembly File Operation Examples](https://eng.libretexts.org/Bookshelves/Computer_Science/Programming_Languages/Book%3A_x86-64_Assembly_Language_Programming_with_Ubuntu_(Jorgensen)/13%3A_System_Services/13.8%3A_File_Operations_Examples)
- [Linux Syscall Table](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)