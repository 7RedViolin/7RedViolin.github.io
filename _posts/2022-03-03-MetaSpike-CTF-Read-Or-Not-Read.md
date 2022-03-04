---
layout: page
title: "MetaSpike CTF 2022 - To Read or Not to Read"
date: 2022-03-03 21:00:00 -0500
tags: ctf email metaspike-2022
intro: What can email headers tell us from a Google Takeout collection?
---

This is a two part challenge from the first week of the MetaSpike CTF (an email-only forensics CTF). Hopefully this will be an ongoing series as new challenges are released each week. You can find my other write ups using the tag [#metaspike-2022](/tags#metaspike-2021). 

## Objective #1
> You have exported the contents of a Google mailbox via Takeout. Looking at the exported data, you suspect that one of the top-level messages may have been read by the perpetrator. 
> Enter its Message-ID (i.e., the value of its "Message-ID:" header field as defined in RFC 5322).

Using Google's Takeout feature, data can be formatted in CSV, JSON, or MBOX (depending on the info to be exported). In our case, we got an MBOX file which is basically EML files separated by two consecutive empty lines. 

When checking the top 20 or so lines of the file, I noticed there was a X-Gmail-Labels header that included tags like "Inbox" and "Unread". 

```
$ head -20 results.mbox
From 1723853304940284153@xxx Fri Feb 04 17:10:22 +0000 2022
X-GM-THRID: 1723853304940284153
X-Gmail-Labels: Inbox,Category Promotions,Unread
Delivered-To: ornatdilwen@gmail.com
Received: by 2002:a05:6a10:8666:0:0:0:0 with SMTP id d6csp295479pxo;
        Fri, 4 Feb 2022 09:10:22 -0800 (PST)
X-Google-Smtp-Source: ABdhPJwIZLo1PamTOO0SX8qR1dEAoQPQ9N/2D/wo1zPZ4sCLhMqXX4tk3HD7nr9xoEC18DU6XzqJ
X-Received: by 2002:a62:1707:: with SMTP id 7mr4170204pfx.18.1643994622308;
        Fri, 04 Feb 2022 09:10:22 -0800 (PST)
ARC-Seal: i=1; a=rsa-sha256; t=1643994622; cv=none;
        d=google.com; s=arc-20160816;
        b=h/e6Sx3kZp8c2vM4m4oTQYToL6aNh02MSWDWX6dEf4X/qJis77Ii0mZ4m2R7jXYiB6
         Ta/HEFgM0Ec9K2nDv6CeEwUveCkGBPu4zWMw579AxrVRQyw+KnDkrn1NdhZJt2Ea4Bla
         sovnX4BmjhKymzb8mK2DQD9v7oCR0xgGLdLJFH4NMHh2HbvjWg0UZCc9fkNM1c3WHkVU
         ONIJPn27A2bSXHAdcFXXs2BRD84/3arPOTjd8wk7pOrd+3hDkhJmXpKIOF63Z1Pv6IQs
         zlyaZlkN6MuhtjaLg9pGphFY2rnkrPc2+/0ADN5vKm/s437R9u07CGhgC/WoGcJHYgxc
         xukw==
ARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;
        h=to:reply-to:subject:message-id:mime-version:from:date
         :dkim-signature:dkim-signature;
```

Since my goal was to find read emails, I tried grepping for the keyword "Read" or any emails missing the "Unread" tag but without any luck.

```
$ grep "X-Gmail-Labels: " results.mbox | grep "Read"
$ grep "X-Gmail-Labels: " results.mbox | grep -v "Unread"
```

But what if the perpetrator switched the flag back to "unread" on the target message after reading? I then ran a check against all the unique values.

```
$ grep "X-Gmail-Labels: " results.mbox | sort | uniq -c
   1217 X-Gmail-Labels: Inbox,Category Promotions,Unread
    586 X-Gmail-Labels: Inbox,Category Updates,Unread
      1 X-Gmail-Labels: Inbox,Opened,Category Updates,Unread
      5 X-Gmail-Labels: Spam,Category Promotions,Unread
      3 X-Gmail-Labels: Spam,Category Updates,Unread
```

And voila! There's an "Opened" label - now it was just a matter of finding the MessageID for that email.

```
$ grep "X-Gmail-Labels: Inbox,Opened,Category Updates,Unread" -A75 -B3 results.mbox

From 1715621750591625172@xxx Fri Nov 05 20:33:20 +0000 2021
X-GM-THRID: 1715621750591625172
X-Gmail-Labels: Inbox,Opened,Category Updates,Unread
Delivered-To: ornatdilwen@gmail.com
Received: by 2002:a05:6a10:870e:0:0:0:0 with SMTP id n14csp69171pxr;
        Fri, 5 Nov 2021 13:33:20 -0700 (PDT)

...

Subject: =?utf-8?Q?Numerical=20Values?=
From: =?utf-8?Q?NextDraft?= <dave@davenetics.com>
Reply-To: =?utf-8?Q?NextDraft?= <dave@davenetics.com>
To: <ornatdilwen@gmail.com>
Date: Fri,  5 Nov 2021 19:47:56 +0000
Message-ID: <ed102783e87fee61c1a534a9d.3e6e597ee0.20211105194751.39849bd368.47d20790@mail199.atl61.mcsv.net>
X-Mailer: MailChimp Mailer - **CID39849bd3683e6e597ee0**
X-Campaign: mailchimped102783e87fee61c1a534a9d.39849bd368
X-campaignid: mailchimped102783e87fee61c1a534a9d.39849bd368
```

So the answer was `<ed102783e87fee61c1a534a9d.3e6e597ee0.20211105194751.39849bd368.47d20790@mail199.atl61.mcsv.net>`

## Objective #2
> Congrats on locating that message!
> You are now examining the message you identified during the first part of this challenge. One of the header fields gives you pause about the authenticity of the message. Which header field is it?
> Enter the name of the header field, including the colon.

I could have used grep to extract that email to make analysis easier but, instead, I used a slightly modified python script to extract the EML files from the MBOX format.

From there, I then used another python script to extract only the header information to make it easier to read and copy/paste into a header analysis tool.

Using MXToolbox, I saw some DKIM failures but that was expected with Gmail. I also tested the headers against two other analyzers and didn't see any DKIM issues.

One thing that stood out to me was the time it took between the first and second hop (almost 45 minutes) so I tested the "X-Received" field but no success. Looking back, delayed email isn't really a suspicious/malicious indicator but then hindsight is 20/20.

A comparison of the Reply-To/From and Delivered/To all matched as expected. Also, Nnothing stood out as suspicious with the MailChimp custom headers (plus documentation out on the internet, or lack thereof, wasn't helpful) so that left the content attributes. Content-Type matched what I saw in the email body but I hadn't checked the Content-Length. By extracting the email body, I was able to run a quick word count and discover about 3,000 extra characters had been added since the headers were generated.

```
$ tail -2 email_header.eml 
Content-Length: 117298
MIME-Version: 1.0

$ wc email_body.eml 
  2179   8477 120872 email_body.eml
```

So the answer was `Content-Length:`

## References
- [Message Read Status](https://www.metaspike.com/message-read-status-gmail-google-workspace/)
- [mbox2eml script](https://github.com/7RedViolin/mbox2eml)
- [eml_header_parser script](https://github.com/7RedViolin/eml_header_parser)
- [MXToolbox Email Header Analyzer](https://mxtoolbox.com/Public/Tools/EmailHeaders.aspx?  huid=9c9e9529-bc88-4f25-8073-0a1fb8a8ca7d)
- [GoogleApps Email Header Analyzer](https://toolbox.googleapps.com/apps/messageheader/analyzeheader)
- [GitHub Project Email Header Analyzer](https://mha.azurewebsites.net/)
- [Content-Length Header Field](https://www.metaspike.com/content-length-header-field-email-forensics/)