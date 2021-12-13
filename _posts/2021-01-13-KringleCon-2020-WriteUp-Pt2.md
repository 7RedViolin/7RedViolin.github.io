---
layout: page
title: "KringleCon 3: French Hens WriteUp - Part 2"
date: 2021-01-13 21:00:00 -0600
tags: ctf regex reverse-engineering network coding cryptography
intro: Welcome back! Here's part two of my write up for the 2020 Holiday Hack Challenge. This will be dedicated to the side quests and will include not only solutions but also references I used to solve the problems. I didn’t make it through all the available problems but what I did complete is outlined here.
---
![Logo](/images/kringlecon2020_obj/logo.PNG)  
## Introduction
Welcome back! Here's part two of my write up for the 2020 Holiday Hack Challenge. This will be dedicated to the side quests and will include not only solutions but also references I used to solve the problems. I didn’t make it through all the available problems but what I did complete is outlined here.

## Side Quests
### Unescape tmux – Pepper Minstix
![](/images/kringlecon2020_sidequests/unescape_tmux_scene.png)  
#### Solution
![](/images/kringlecon2020_sidequests/unescape_tmux_opening.png)  
Using the ls command, I could see there was an existing tmux instance. I attached to that instance and found the target image.  
![](/images/kringlecon2020_sidequests/unescape_tmux_answer.png)  
#### References
https://tmuxcheatsheet.com/

### Sort-O-Matic – Minty Candycane
![](/images/kringlecon2020_sidequests/sort_o_matic_scene.png)  
#### Solution
Once I got to the workshop (level 1.5), I found the Sort-O-Matic that was on the fritz and not sorting toys properly due to bad regex.  

**Problem 1:** Matches at least one digit  
**Answer:** `\d+`  
**Explanation:** `\d` is short for all single digits 0 to 9. + means one or more occurrences of the pattern prior to the `+`.  

**Problem 2:** Matches 3 alpha a-z characters ignoring case  
**Answer:** `[a-zA-Z]{3}`  
**Explanation:** `[a-zA-Z]` is short for any upper or lowercase letter in the alphabet. `{3}` means exactly three occurrences of the pattern prior to the `{3}`.  

**Problem 3:** Matches 2 chars of lowercase a-z or numbers  
**Answer:** `[a-z0-9]{2}`  
**Explanation:** `[a-z0-9]` is short for any lowercase letter in the alphabet or any single digit 0 to 9. `{2}` means exactly two occurrences of the pattern prior to the `{2}`.  

**Problem 4:** Matches any 2 characters no uppercase A-L or 1-5  
**Answer:** `[^A-L1-5]{2}`  
**Explanation:** `[^A-L1-5]` is short for any uppercase letter A to L or single digit 1 – 5. The `^` in the beginning of the bracketed section is used as a “not” or “exclude”. `{2}` means exactly two occurrences of the pattern prior to the `{2}`.  

**Problem 5:** Matches three or more digits only  
**Answer:** `^\d{3,}$`  
**Explanation:** `^` means the string must start with the following pattern. `\d` is short of any single digit from 0 to 9. `{3,}` means 3 or more occurrences of the pattern prior to the `{3,}`. `$` means the string must end the with pattern prior to the `$`.  

**Problem 6:** Matches multiple hour:minute:second time formats only  
**Answer:** `^(([0-1]?[0-9])|([2][0-3]))(\:[0-5][0-9]){2}$`  
Explanation: ^ means the string must start with the following pattern. The next phrase ([0-1]?[0-9]) means the first digit must be 0 or 1 if the second digit is between 0 and 9. The second phrase ([2][0-3]) means the first digit can only be a 2 if the second digit is between 0 and 3. The last phrase (\:[0-5][0-9]){2}$ means the string must end with two sets of two digit numbers between 00 and 59 each prepended with a “:”.  

**Problem 7:** Matches MAC address format only while ignoring case  
**Answer:** ^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$  
**Explanation:** ^ means the string must start with the following pattern. The next phrase ([0-9a-fA-F]{2}:){5} means there must be five sets of two digit hexadecimal numbers (case insensitive) with each set appended with a “:”. The last phrase [0-9a-fA-F]{2}$ means the string must end with one set of two digit hexadecimal number.  

**Problem 8:** Matches multiple month, day, and year formats only  
**Answer:** ^(([0-2][0-9])|([3][0-1]))(\.|\/|\-)(([0][1-9])|([1][0-2]))(\.|\/|\-)[0-9]{4}$  
**Explanation:** ^ means the string must start with the following pattern. The next phrase (([0-2][0-9])|([3][0-1])) (\.|\/|\-) means there must be a two digit number ranging from 00 to 31 followed by either a “.” or “/” or “–”. The phrase (([0][1-9])|([1][0-2])) (\.|\/|\-) means there must be a two digit number ranging from 01 to 12 followed by either a “.” or “/” or “–”. The last phrase [0-9]{4}$ means the string must end with a four digit number.  

### References
https://regex101.com/  
https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples649dc1c3f285

## Speaker UNPrep – Bushy Evergreen
![](/images/kringlecon2020_sidequests/speaker_unprep_scene.png)  
### Solution
Here was a fun little game to unlock the UnPrep room, turn on the lights, and fix the vending
machine.  
![](/images/kringlecon2020_sidequests/speaker_unprep_door1.png)  
Hoping the error/failure might give a hint, I ran the door program. But no luck.  
![](/images/kringlecon2020_sidequests/speaker_unprep_door2.png)  
My next step was to grep through the door script for the password in plaintext.  
![](/images/kringlecon2020_sidequests/speaker_unprep_door3.png)  
![](/images/kringlecon2020_sidequests/speaker_unprep_door4.png)  
The next puzzle was to turn on the lights. However, this time a configuration file was involved.  
I tried to put in the literal string from the password field but that didn’t work.  
![](/images/kringlecon2020_sidequests/speaker_unprep_lights1.png)  
I decided to go to the lab folder and see if I could play around with this to see what’s up with the password field in the config file. My next attempt was to edit the password field in the configuration file in the lab environment to determine the encryption method without success.

I kept at it until I was about to pull my hair. Then I had a brain spark: What if, in the lab setting, I set the username and password to the same encrypted string? I recalled that when the program was run, it mentioned decrypting select fields from the configuration file.  
![](/images/kringlecon2020_sidequests/speaker_unprep_lights9.png)  
![](/images/kringlecon2020_sidequests/speaker_unprep_lights10.png)  
It was that simple!  
![](/images/kringlecon2020_sidequests/speaker_unprep_lights11.png)  
Now I had to tackle the vending machine problem . . .  
![](/images/kringlecon2020_sidequests/speaker_unprep_vending1.png)  
The password in the config was obviously encrypted.  
![](/images/kringlecon2020_sidequests/speaker_unprep_vending2.png)  
But the hint was to remove the config file. I followed the hint and was then prompted by the program to create a new config.  
![](/images/kringlecon2020_sidequests/speaker_unprep_vending3.png)  
When I opened the newly created config file, I saw a different encoded password.  
![](/images/kringlecon2020_sidequests/speaker_unprep_vending4.png)  
The best way I knew how to solve this was to use brute force through various iterations of AAAAAAAA, BBBBBBBB, CCCCCCCC, etc.  
The final result was . . . CandyCane1 – and it only took three hours. What I won’t do for a CTF . . .  
![](/images/kringlecon2020_sidequests/speaker_unprep_vending5.png)  

## Can Bus Investigation – Wunrose Openslae
![](/images/kringlecon2020_sidequests/canbus_scene.png)  
### Solution
![](/images/kringlecon2020_sidequests/canbus_opening.png)  
To get an idea of the format of the log, I just grabbed the first 10 lines of candump.log which appeared to be space delimited.  
![](/images/kringlecon2020_sidequests/canbus_answer1.png)  
According to the KringleCon talk, the third column is of the most interest. With “cut”, I was able to pull out that information and sort/dedupe to figure out what commands were run exactly three times with two different data outputs.  
![](/images/kringlecon2020_sidequests/canbus_answer2.png)  
In the above image, I cut off the full page as it went on for quite a while. What I was most interested in what the 19B events as that matched the search criteria. Since the UNLOCK command was run only once, I assumed 19B#00000F000000 was the target. Using grep, I pulled the timestamp (in UNIX format).  
![](/images/kringlecon2020_sidequests/canbus_answer3.png)  
It took a couple tries but I finally figured out the right format for the answer.  
![](/images/kringlecon2020_sidequests/canbus_answer4.png)  
### References
https://www.youtube.com/watch?v=96u-uHRBI0I
## 33.6kbps – Fitzy Shortstack
![](/images/kringlecon2020_sidequests/336kbps_scene.png)
### Solution
This puzzle was to answer the phone using modem sounds.  
![](/images/kringlecon2020_sidequests/336kbps_opening.png)  
From the code, I could see the order of events to solve the challenge were:  
1. Dialing the correct number  
![](/images/kringlecon2020_sidequests/336kbps_code1.png)  
2. Clicking the options in the following order  
![](/images/kringlecon2020_sidequests/336kbps_code2.png)  
![](/images/kringlecon2020_sidequests/336kbps_code3.png)  
![](/images/kringlecon2020_sidequests/336kbps_code4.png)  
![](/images/kringlecon2020_sidequests/336kbps_code5.png)  
![](/images/kringlecon2020_sidequests/336kbps_code6.png)  
The CSS of the webpage told me the positions of each button on the opening screen:  

| Button Name | Rotation | Image |
| ---- | ---- | ---- |
| respCrEsCl | +1 deg | baaDEEbrrr |
| Ack | -8 deg | aaah |
| Cm_cj | +2 deg | WEWEWwrwrrwrr |
| 11_12_info | -6 deg | beDURRdunditty |
| Trn | + 5 deg | SCHHRRHHRTHRTR |

![](/images/kringlecon2020_sidequests/336kbps_code7.png)  

## Scapy Prepper – Alabaster Snow
![](/images/kringlecon2020_sidequests/scapy_scene.png)
### Solution
This is just a test of scapy knowledge and the solution is pretty straight forward. At the end, I’ve included sites I used as reference.  
![](/images/kringlecon2020_sidequests/scapy_problem1.png)  
![](/images/kringlecon2020_sidequests/scapy_problem2.png)  
![](/images/kringlecon2020_sidequests/scapy_problem3.png)  
![](/images/kringlecon2020_sidequests/scapy_problem4.png)  
![](/images/kringlecon2020_sidequests/scapy_problem5.png)  
![](/images/kringlecon2020_sidequests/scapy_problem6.png)  
![](/images/kringlecon2020_sidequests/scapy_problem7.png)  
![](/images/kringlecon2020_sidequests/scapy_problem8.png)  
![](/images/kringlecon2020_sidequests/scapy_problem9.png)  
![](/images/kringlecon2020_sidequests/scapy_problem10.png)  
![](/images/kringlecon2020_sidequests/scapy_problem11.png)  
![](/images/kringlecon2020_sidequests/scapy_problem12.png)  
![](/images/kringlecon2020_sidequests/scapy_problem13.png)  
![](/images/kringlecon2020_sidequests/scapy_problem14.png)  
![](/images/kringlecon2020_sidequests/scapy_problem15.png)  
![](/images/kringlecon2020_sidequests/scapy_problem16.png)  
### References
https://scapy.readthedocs.io/en/latest/api/scapy.utils.html  
https://scapy.readthedocs.io/en/latest/api/scapy.sendrecv.html  
https://0xbharath.github.io/art-of-packet-crafting-withscapy/scapy/creating_packets/index.html  

### Elf Coder – Ribb Bonbowford
![](/images/kringlecon2020_sidequests/elf_coder_scene.png)  
This puzzle required some JavaScript knowledge to get the video game elf to the capture the lollipops while avoiding munchkins, obstacles, pits, and yeeters.  

**Challenge 1**
![](/images/kringlecon2020_sidequests/elf_coder_challenge1.png)  
**Restrictions:** Program the elf to the end goal in no more than 2 lines of code and no more
than 2 elf commands.

**Code:**  
```javascript
elf.moveLeft(10)  
elf.moveUp(10)
```

**Challenge 2**
![](/images/kringlecon2020_sidequests/elf_coder_challenge2.png)  
**Restrictions:** Program the elf to the end goal in no more than 5 lines of code and no more
than 5 elf command/function execution statements in your code.  

**Lever Objective:** Add 2 to the numeric value of the running function elf.get_lever(0)

**Code:**
```javascript
elf.moveTo(lever[0])  
elf.pull_lever(elf.get_lever(0) + 2)  
elf.moveLeft(4)  
elf.moveUp(10)  
```

**Challenge 3**
![](/images/kringlecon2020_sidequests/elf_coder_challenge3.png)  
**Restrictions:** Program the elf to the end goal in no more than 4 lines of code and no more
than 4 elf command/function execution statements in your code.  

**Code:**  
```javascript
elf.moveTo(lollipop[0])  
elf.moveTo(lollipop[1])  
elf.moveTo(lollipop[2])  
elf.moveUp(1)
```

**Challenge 4**
![](/images/kringlecon2020_sidequests/elf_coder_challenge4.png)  
**Restrictions:** Program the elf to the end goal in no more than 7 lines of code and no more
than 6 elf command/function execution statements in your code.  

**Code:**  
```javascript
elf.moveLeft(1)  
for (i = 0; i <= 4; i++) {  
  elf.moveUp(40)  
  elf.moveLeft(3)  
  elf.moveDown(40)   
  elf.moveLeft(3)  
}
```

**Challenge 5**
![](/images/kringlecon2020_sidequests/elf_coder_challenge5.png)  
**Restrictions:** Program the elf to the end goal in no more than 10 lines of code and no more
than 5 elf command/function execution statements in your code.  

**Munchkin Objective:** Remove non-numeric elements from the array provided and return to
the munchkin.  

**Code:**
```javascript
elf.moveTo(lollipop[1])
elf.moveTo(lollipop[0])
elf.tell_munch(elf.ask_munch(0).filter(word =>
Number.isInteger(word)))
elf.moveUp(10)
```

**Challenge 6**
![](/images/kringlecon2020_sidequests/elf_coder_challenge6.png)  
**Restrictions:** Program the elf to the end goal in no more than 15 lines of code and no more
than 7 elf command/function execution statements in your code.  

**Lever Objective:** Prepend “munchkins rule” to the provided array and return to the lever.
Munchkin Objective: Find the key in the provided JSON object with the value “lollipop”
and return to the munchkin.  

**Code (for Lever):**
```javascript
for (i = 0; i < 4; i++) {
  elf.moveTo(lollipop[i])
}
elf.moveTo(lever[0])
elf.pull_lever(["munchkins rule"].concat(elf.get_lever(0)))
elf.moveDown(3)
elf.moveLeft(6)
elf.moveUp(40)
```

**Code (for Munchkin):**
```javascript
for (i = 0; i < 4; i++) {
  elf.moveTo(lollipop[i])
}
elf.moveTo(munchkin[0])
var temp = elf.ask_munch(0)
for (x in temp) {
  if (temp[x] == "lollipop") {
   elf.tell_munch(x)
  }
}
elf.moveUp(40)
```

**Challenge 7 (Bonus 1)**
![](/images/kringlecon2020_sidequests/elf_coder_challenge7.png)  
**Restrictions:** Program the elf to the end goal in no more than 25 lines of code and no more than 10 elf command/function execution statements in your code. Note elf.moveTo(object) has been disabled for this challenge.  

**Lever Objective:** None. Levers can be pulled without passing solutions to them.  

**Munchkin Objective:** Create a function that will accept one object – a randomized array containing arrays of strings and numbers. The function must iterate over the array and its child arrays and return the total sum of adding all the numbers in all the child arrays.

**Code:**
```javascript
function munchkin_solver(temp) {
  var result = 0;
  for (i = 0; i < temp.length; i++) {
   result += temp[i].filter(word => Number.isInteger(word)).reduce((x, y) => x + y)
  }
  return result
}
for (i = 0; i < 8; i++) {
  if (i % 4 == 0) {
    elf.moveDown(i + 1)
  } else if (i % 4 == 1) {
    elf.moveLeft(i + 1)
  } else if (i % 4 == 2) {
    elf.moveUp(i + 1)
  } else {
    elf.moveRight(i + 1)
  }
  elf.pull_lever(i)
}
elf.moveUp(2)
elf.moveLeft(4)
elf.tell_munch(munchkin_solver)
elf.moveUp(40)
```

**Challenge 8 (Bonus 2)**
![](/images/kringlecon2020_sidequests/elf_coder_challenge8.png)
**Restrictions:** Program the elf to the end goal in no more than 40 lines of code and no more than 10 elf command/function execution statements in your code. Note elf.moveTo(object) function has been disabled for this challenge.

**Lever Objective:** Each lever will return a number. Sum the numbers for all past levers and return to current lever. For example: lever0_value + lever1_value + lever2_value = lever2_solution

**Munchkin Objective:** Create a function that will accept one object – a randomized array containing json objects. The function must iterate over the array of json objects and return the key contains the value “lollipop”.

**Code:**
```javascript
function munchkin_solver(temp) {
  var result = ""
  for (i = 0; i < temp.length; i++) {
    var other = temp[i]
    for (x in other) {
      if (other[x] == "lollipop") {
        result = x
      }
    }
  }
  return result
}
var num = 0;
for (i = 1; i < 7; i++) {
  if (i % 2 == 0) {
    elf.moveLeft((2 * i) - 1)
  } else {
    elf.moveRight((2 * i) - 1)
  }
  num += elf.get_lever(i - 1)
  elf.pull_lever(num)
  elf.moveUp(2)
}
elf.tell_munch(munchkin_solver)
elf.moveRight(40)
```

### References
https://developer.mozilla.org/enUS/docs/Web/JavaScript/Reference/Global_Objects/Array/filter  
https://developer.mozilla.org/enUS/docs/Web/JavaScript/Reference/Global_Objects/Number/isInteger  
https://www.w3schools.com/jsref/jsref_concat_array.asp  
https://www.w3schools.com/js/js_json_objects.asp

## Snowball Game – Tangle Coalbox
![](/images/kringlecon2020_sidequests/snowball_scene.png)

### Solution
For this puzzle, the goal is to beat the Snowball Fight game on the Impossible Level. However, at that level, the computer never misses so I have to somehow know the answers in advance.  
![](/images/kringlecon2020_sidequests/snowball_opening.png)  
After playing a couple times on different levels and reading through the hints, the game appears to use the Mersenne Twister algorithm to generate player names on the Impossible level. Opening the source code for an impossible level game shows the seed attempts:  
![](/images/kringlecon2020_sidequests/snowball_seeds1.png)  
![](/images/kringlecon2020_sidequests/snowball_seeds2.png)  
This required the MT19937 predictor to figure out the redacted number. For more information on how to set up the MT19937 predictor command and its usage, see my previous post KringleCon 2020 Part 1 section Objective 11a.  
![](/images/kringlecon2020_sidequests/snowball_prediction1.png)  
![](/images/kringlecon2020_sidequests/snowball_prediction2.png)  
With the player name in hand, I opened another instance of the snowball game in a separate browser using the URL https://snowball2.kringlecastle.com/game. I set up an easy level game with the player name set to 1140973051 so I could use trial and error to find the answers and beat the computer on the impossible level.  
![](/images/kringlecon2020_sidequests/snowball_answer1.png)  
Once I was entered the final square (6,9), I won the game!  
![](/images/kringlecon2020_sidequests/snowball_answer2.png)  

### References
https://github.com/kmyk/mersenne-twister-predictor
