---
layout: page
title: "Holiday Hack Challenge 2024 WriteUp - Hardware Hacking 101 Part 1"
date: 2024-11-24 21:00:00 -0500
tags: ctf hhc-2024 hardware
intro: Jingle all the wires and connect to Santa's Little Helper to reveal the merry secrets locked in his chest!
---

## Background Information

> Hello there! I’m Jewel Loggins.
> 
> I hate to trouble you, but I really need some help. Santa’s Little Helper tool isn’t working, and normally, Santa takes care of this… but with him missing, it’s all on me.
> 
> I need to connect to the UART interface to get things running, but it’s like the device just refuses to respond every time I try.
> 
> I've got all the right tools, but I must be overlooking something important. I've seen a few elves with similar setups, but everyone’s so busy preparing for Santa’s absence.
> 
> If you could guide me through the connection process, I’d be beyond grateful. It’s critical because this interface controls access to our North Pole access cards!
> 
> We used to have a note with the serial settings, but apparently, one of Wombley’s elves shredded it! You might want to check with Morcel Nougat—he might have a way to recover it.

## Silver Objective

In this objective, I needed to configure the Santa's Little Helper device but troubleshooting the settings was going to be impossible without more information.

From the previous challenge [Frosty Keypad](https://7redviolin.github.io/2024/11/23/HolidayHackChallenge-2024-WriteUp-FrostyKeypad.html), I got a collection of shredded paper that needed to be reconstructed that could tell me the exact values needed to get the tool up and running.

This was an easy challenge because one of the hints linked to a [handy python script](https://gist.github.com/arnydo/5dc85343eca9b8eb98a0f157b9d4d719) to reconstruct the image using [heuristic edge detection](https://en.wikipedia.org/wiki/Edge_detection).

![initial assembled image](/images/holidayhackchallenge2024/initial_assembled_image.png)

Long story short, I got a good first pass that needed just a bit of Microsoft Paint magic to make it easily readable by flipping the image across the vertical line

![assembled image final](/images/holidayhackchallenge2024/assembled_image_final.png)

Now it was just a matter of connecting the wires and configuring the settings per the restored picture. This step took longer than I like to admit because I didn't initially realize the receiving and transmitting pins weren't supposed to be connected 1-to-1 but crossed.

![](/images/holidayhackchallenge2024/hardwarehacking_part1_6.png)

## Gold Objective

In this objective, I was challenged to bypass the hardware altogether. This took a bit of reviewing the client-side Javascript to find an old v1 API mentioned in the comments.

![](/images/holidayhackchallenge2024/hardwarehacking_part1_7.png)

The trick was figuring out the correct values and order that should be passed in the `series` variable. I eventually resorted to debugging the code and setting a breakpoint where the post request is made to capture the information.

![](/images/holidayhackchallenge2024/hardwarehacking_part1_8.png)

From there, I built out a quick Python script to complete the Gold level.

```python
import requests
import time
import json
import sys

headers = {"Content-Type": "application/json"}

serial = [3, 9, 2, 2, 0, 3]

payload = json.dumps({ "requestID": "fd4d1d67-b790-4b26-ac02-cf271386a09b", "serial": serial, "voltage": 3 })

response = requests.post('https://hhc24-hardwarehacking.holidayhackchallenge.com/api/v1/complete', data=payload, headers = headers)

print(response.text)
```

## Easter Egg

As I worked with the shredded paper, I noticed there were comments added to each JPG file that appeared to be base64 encoded. 

![](/images/holidayhackchallenge2024/hardwarehacking_part1_3.png)

Throwing it into CyberChef confirmed my suspicions.

![](/images/holidayhackchallenge2024/hardwarehacking_part1_4.png)

At first, I assumed these strings needed to be joined based on how the shreds were arranged for the completed image. However, that resulted in gibberish so it was back to the drawing board.

I then noticed the first element of each decoded string looked to be a reversed base64 encoded string since some of them started with `==`. Back to CyberChef, it showed these decoded to be numbers so I tried ordering the strings based on that index and voila a fun short story popped out - albeit with a few typos since my script wasn't super careful in parsing the data:

![](/images/holidayhackchallenge2024/hardwarehacking_part1_5.png)

It was not an easy feat to figure out how to script access to the comments field but, as with all programming questions, I came across an answer in a [Stack Overflow thread](https://stackoverflow.com/questions/49214905/get-attributes-listed-in-the-details-tab-with-powershell).

```powershell
$folder = 'C:\Users\User\Downloads\shreds\slices'

$shell = New-Object -COMObject Shell.Application
$shellfolder = $shell.Namespace($folder)

$max_count = (Get-ChildItem $folder | Measure-Object).Count

$max_count

$answers = 0..$max_count

Get-ChildItem $folder | Select-Object Name | %{
    $temp = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($shellfolder.GetDetailsOf($shellfolder.ParseName($_.Name), 24))).replace('"', "").replace("[", "").replace("]", "").replace(", ", ",").split(",")
    $temp1 = $temp[0].ToCharArray()
    [array]::Reverse($temp1)
    $index =  [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(-join($temp1)))
    $answers[$index] = $temp[1]
}

-join($answers)
```

```
0Long ago in the snowy realm of the North Pole (not too far away if you're a reindeer) there existed a magical land ruled by a mysterious figure known as the Great Claus. Two spirited elvesTwinkle and Jangleoamed this frosty kingdomdefending it from the perils of holiday chee
rlessness. Twinkle sporting a bright red helmet-shaped hat that tilted just soas quick-witted and even quicker with a snowball. Jangle a bit tallerwore a green scarf that drooped like a sleepy reindeer\u2019s ears. Together they were the Mistletoe Knights the protectors of th
e magical land and the keepers of Claus\u2019 peace. One festive morningthe Great Claus summoned them for a critical quest. 'Twinkleangle the time has comehe announced with a voice that rumbled like thunder across the ice plains. 'The fabled Never-Melting Snowflake a relic th
at grants one wish lies hidden beyond the Peppermint Expanse. Retrieve itand all marshmallow supplies will be secured!' Armed with Jangle\u2019s handmade map (created with crayon and a lot of optimism)he duo set off aboard their tobogganhe Frostwing. Howeverhe map led them in
 endless loops around the Reindeer Academyuch to the amusement of trainee reindeer perfecting their aerial maneuvers. Blitzen eventually intercepted themhuckling 'Lostellas? The snowflake isn\u2019t here. Try the Enchanted Peppermint Grove!' Twinkle facepalmed as Jangle prete
nded to adjust his map. With Blitzen\u2019s directionshey zoomed off again this time on the right course. The Peppermint Grove was alive with its usual enchantments\u2014candy cane trees swayed and sang ancient ballads of epic sleigh battles and the triumphs of Claus\u2019 ca
ndy cane squadrons. Twinkle and Jangle joined the peppermint choirheir voices harmonizing with the festive tune. Hours laterthe duo stumbled upon a hidden cave guarded by giant gumdrop sentinels (luckily on their lunch break). Insidethe air shimmered with Claus\u2019 magic. T
here it was\u2014the Never-Melting Snowflake glistening on a pedestal of ice. Twinkle\u2019s eyes widened 'We\u2019ve found itJangle! The key to infinite marshmallows!' As Twinkle reached for the snowflakea voice boomed from the cave walls'One wishou have. Choose wisely or fa
ce the egg-nog of regret.' Without hesitationJangle exclaimed'An endless supply of marshmallows for our cocoa!' The snowflake glowed and with a burst of magic marshmallows poured downcovering the cave in a fluffy sweet avalanche. Back at the workshop the elves were hailed as 
heroes\u2014the Marshmallow Knights of Claus. They spent the rest of the season crafting new cocoa recipes and sharing their bounty with all. And sounder the twinkling stars of the northern skies Twinkle and Jangle continued their adventurestheir mugs full of cocoaheir hearts
 full of joy and their days full of magic. For in the North Poleevery quest was a chance for festive fun and every snowflake was a promise of more marshmallows to come.
```