---
layout: page
title: "Shakti CTF 2021 Pillow Challenge WriteUp"
date: 2021-04-06 13:00:00 -0000
tags: ctf coding
intro: This was an awesome beginner CTF that has an accompanying conference called ShaktiCon - a free international conference dedicated to women in cybersecurity. This specific puzzle required some python coding skills.
---
This was an awesome beginner CTF that has an accompanying conference called [ShaktiCon](https://shakticon.com/). This is a free international conference dedicated to women in cybersecurity.

I focused on the forensic and miscellaneous challenges which were above beginner but not, from my experience, fully intermediate-level. I plan to attend next year and would highly recommend this to others.

## Miscellaneous Challenge: Pillow
> Fix them up and get your flag!

For this challenge, we were given 3,000 10x10 jpg files. The clue was 60x50 so I assume we need to arrange these files like tiles in a mosaic.

Dear friendly Google came to the rescue and showed that there has been a similar question posed on [StackOverflow](https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python).  Basically, the suggested solutions use the [Python Image Library (PIL)](https://pillow.readthedocs.io/en/stable/index.html) to manipulate image files.

Using the StackOverflow answers as the base, I made a [script](/supporting_files/shaktictf2021/pillow_solver.py) that iterated through all the images and stitched them into rows of 50. The script then joined the rows together vertically to create a 500-pixel wide by 600-pixel tall image.

![](/images/shaktictf2021/pillow_1.png)

To view the image correctly, I used GIMP to rotate and flip the picture to get the flag `shaktictf{pill0w_lik3_a_g00d_c0nscience}`

![](/images/shaktictf2021/pillow_2.png)