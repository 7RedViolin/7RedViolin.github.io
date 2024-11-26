---
layout: page
title: "Holiday Hack Challenge 2024 WriteUp - Hardware Hacking 101 Part 2"
date: 2024-11-22 21:00:00 -0500
tags: ctf hhc-2024 hardware
intro: Santa’s gone missing, and the only way to track him is by accessing the Wish List in his chest—modify the access_cards database to gain entry!
---

## Silver Objective

Our goal here was to grant card number 42 with full access using the Santa's Little Helper (SLH) terminal tool.

![](/images/holidayhackchallenge2024/hardwarehacking_part2_3.png)

First, I tried just straight up setting the access but of course this challenge wasn't that easy to solve.

```bash
slh@slhconsole\> slh --set-access 1 --id 42
Invalid passcode. Access not granted.
```

I needed credentials and the hint was: 

> It is so important to keep sensitive data like passwords secure. Often times, when typing passwords into a CLI (Command Line Interface) they get added to log files and other easy to access locations. It makes it trivial to step back in history and identify the password.

This made me think of the `history` command that allows you to see recent commands executed in the terminal.

```bash
slh@slhconsole\> history
    1  cd /var/www/html
    2  ls -l
    3  sudo nano index.html
    4  cd ..
    5  rm -rf repo
    6  sudo apt update
    7  sudo apt upgrade -y
    8  ping 1.1.1.1
    9  slh --help
   10  slg --config
   11  slh --passcode CandyCaneCrunch77 --set-access 1 --id 143
   12  df -h
   13  top
   14  ps aux | grep apache
   15  sudo systemctl restart apache2
   16  history | grep ssh
   17  clear
   18  whoami
   19  crontab -e
   20  crontab -l
   21  alias ll='ls -lah'
   22  unalias ll
   23  echo "Hello, World!"
   24  cat /etc/passwd
   25  sudo tail -f /var/log/syslog
   26  mv archive.tar.gz /backup/
   27  rm archive.tar.gz
   28  find / -name "*.log"
   29  grep "error" /var/log/apache2/error.log
   30  history
```

And wouldn't you know it on line 11, we see someone else ran `slh` and entered the password in clear text.

So to complete this objective, I simply needed to run the following command

![](/images/holidayhackchallenge2024/hardwarehacking_part2_4.png)

## Gold Objective

For this, I needed to make the same change to access card 42 but this time going directly to the database.

I noticed there was an `access_cards` file in the current directory and when running the `file` command, it looked to be a SQLite database

```bash
slh@slhconsole\> ls -al
total 156
drwxrwxr-t 1 slh  slh    4096 Nov 26 02:06 .
drwxr-xr-x 1 root root   4096 Nov 13 14:44 ..
-r--r--r-- 1 slh  slh     518 Oct 16 23:52 .bash_history
-r--r--r-- 1 slh  slh    3897 Sep 23 20:02 .bashrc
-r--r--r-- 1 slh  slh     807 Sep 23 20:02 .profile
-rw-r--r-- 1 root root 131072 Nov 26 02:06 access_cards
```

```bash
slh@slhconsole\> file access_cards
access_cards: SQLite 3.x database, last written using SQLite version 3040001, file counter 5, database pages 32, cookie 0x2, schema 4, UTF-8, version-valid-for 5
```

So from there, I ran the command `sqlite3 access_cards` to open a session with the database and start poking around.

My first command was to see what tables were available

```bash
sqlite> .tables
access_cards  config
```

The `access_cards` table was pretty much expected but I did want to verify the columns

```bash
sqlite> pragma table_info(access_cards);
0|id|INTEGER|0||1
1|uuid|TEXT|0||0
2|access|INTEGER|0||0
3|sig|TEXT|0||0
```

Then, I moved on to look at the `config` table and what it contained

```bash
sqlite> pragma table_info(config); 
0|id|INTEGER|0||1
1|config_key|TEXT|0||0
2|config_value|TEXT|0||0
sqlite> select * from config;
1|hmac_secret|9ed1515819dec61fd361d5fdabb57f41ecce1a5fe1fe263b98c0d6943b9b232e
2|hmac_message_format|{access}{uuid}
3|admin_password|3a40ae3f3fd57b2a4513cca783609589dbe51ce5e69739a33141c5717c20c9c1
4|app_version|1.0
```

So it not only gave me the HMAC secret but also the message format I needed to use when throwing this into CyberChef.

![](/images/holidayhackchallenge2024/hardwarehacking_part2_2.png)

From there, it was simply a matter of running an update command to set the `access` and `sig` field

```bash
sqlite> update access_cards set access = 1, sig='135a32d5026c5628b1753e6c67015c0f04e26051ef7391c2552de2816b1b7096' where id=42;
```

![](/images/holidayhackchallenge2024/hardwarehacking_part2_1.png)