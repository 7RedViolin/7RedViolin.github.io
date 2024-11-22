---
layout: page
title: "Holiday Hack Challenge 2024 WriteUp - Frosty Keypad"
date: 2024-11-22 21:00:00 -0500
tags: ctf hhc-2024
intro: In a swirl of shredded paper, lies the key. Can you unlock the shredder’s code and uncover Santa's lost secrets?
---

## Silver Objective

For this first challenge, we're given the hint we'll need a book to solve the puzzle. Exploring around the front yard, we find a copy of "The Night Before Christmas" lying in the snow not far from the keypad. But there wasn't any obvious highlighting or formatting that told me the code.

![](/images/holidayhackchallenge2024/frostykeypad_1.png)

I then looked at the keypad itself and noticed a sticky note in the upper left hand corner.

![](/images/holidayhackchallenge2024/frostykeypad_2.png)

Being a National Treasure fan, I recognized this as an Ottendorf cipher where the code 2:6:1 meant the second page, sixth word on that page, and first letter of that word.

![](/images/holidayhackchallenge2024/frostykeypad_3.png)

So going from left to right, top to bottom, I got the code `SANTA`. But that's letters and not numbers which led me to the T9 alphabet that maps the alphabet to digits

![](https://www.dcode.fr/tools/phone-keypad/images/keypad.png)

From there, I used the code `72682` and got a lot of shredded paper that needed to be restored but that puzzle was for another challenge. 

## Gold Objective

In the hard level, we were given the hint to use a UV light to find what numbers were actually used. Once again digging around in the snow, I found the UV light and figured out the digits 2, 6, 7, and 8 were used. I decided to write a quick python script to brute force the keypad rather than manually type in the results. Below is the script with comments on nuances.

```python
import requests
import time
import json
import sys

# assume five digits only since the silver objective used five digits
i = 22678
max_num = 88762
array_of_nums = ['2', '6', '7', '8']

while i <= max_num:
  temp = str(i)
  check_pass = 0

  if i != '72682': # added this check so we don't test the code we already know
    for num in array_of_nums:
      if num in temp:
        check_pass += 1
        temp = temp.replace(num, '')

  if (check_pass == 4) & (temp == ''): # only run a check if all four numbers are present without any others
    payload = json.dumps({'answer': f"{i}"})
    response = requests.post('https://hhc24-frostykeypad.holidayhackchallenge.com/submit?id=1ec9fa3f-6b4d-421b-b2e3-288ea40bb717', data=payload, headers={"Content-Type": "application/json"})
    if "error" not in response.text: # if we get a successful message, stop testing other codes
      print(f"{i}: {response.text}")
      sys.exit()
    else: # this else statement is only here so i know the script is working
      print(f"{i}: {response.text}")
    time.sleep(1) # there's a throttle limit of one request per second
  i += 1
```

Answer: `22786`