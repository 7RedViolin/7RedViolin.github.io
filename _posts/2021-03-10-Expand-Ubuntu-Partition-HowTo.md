---
layout: default
title: "Expand Ubuntu Partition HowTo"
date: 2021-03-10 13:00:00 -0000
---

# Expand Ubuntu Partition HowTo

I recently made a basic Ubuntu VM with only 20GB of hard disk space and assumed I would only use it for light testing. As time went on, though, I eventually got the point where I wanted to install REMnux and SIFT on that box rather than create a whole new VM and space was becoming an issue.

So, I began by deleting all snapshots and increasing the VM  size settings by 40GB. However, this new space was still marked "unallocated" and wasn't automatically added to the existing partition. After a lot of trial and error, this is what ended up working for me:

1. Run `fdisk` to begin a log of changes to be made.
```
$ sudo fdisk /dev/sda
```
2. List all partitions using the `p` command. Note that the new 40GB is nowhere to be found in the list. Also, `/dev/sda2` is an extended partition that contains the logical partition `/dev/sda5`.
```
Command (m for help): p
Device     Boot   Start      End  Sectors  Size Id Type
/dev/sda1  *       2048  1050623  1048576  512M  b W95 FAT32
/dev/sda2       1052670 41940991 40888322 19.5G  5 Extended
/dev/sda5       1052672 41940991 40888320 19.5G 83 Linux
```
3. Delete the partitions I want to expand
```
Command (m for help): d
Partition number (1,2,5, default 5): 5
Partition 5 has been deleted.
Command (m for help): d 
Partition number (1,2, default 2): 2
Partition 2 has been deleted.
```
4. Create partition 2 (with default settings) to cover all available space.
```
Command (m for help): n   
Partition type   
p   primary (1 primary, 0 extended, 3 free)   
e   extended (container for logical partitions)
Select (default p): e
Partition number (2-4, default 2): 2
First sector (1050624-125829119, default 1050624): 
Last sector, +/-sectors or +/-size{K,M,G,T,P} (1050624-125829119, default 125829119): 
Created a new partition 2 of type 'Extended' and of size 59.5 GiB.
```
5. Create logical partition 5 (with default settings).
```
Command (m for help): n
All space for primary partitions is in use.
Adding logical partition 5
First sector (1052672-125829119, default 1052672): 
Last sector, +/-sectors or +/-size{K,M,G,T,P} (1052672-125829119, default 125829119): 
Created a new partition 5 of type 'Linux' and of size 59.5 GiB.
Partition #5 contains a ext4 signature.
Do you want to remove the signature? [Y]es/[N]o: Y
The signature will be removed by a write command.
```
6. Finally, enter `w` to write the logged changes and `sudo reboot` to restart the VM.

7. Once the machine is rebooted, `resize2fs` will need to be run against the logical partition to finalize the changes.
```
sudo resize2fs /dev/sda5
resize2fs 1.45.5 (07-Jan-2020)
Filesystem at /dev/sda5 is mounted on /; on-line resizing required
old_desc_blocks = 3, new_desc_blocks = 8
The filesystem on /dev/sda5 is now 15597056 (4k) blocks long.
```
