---
layout: page
title: "KringleCon 4: Four Calling Birds WriteUp - Now Hiring!"
date: 2022-01-21 21:00:00 -0500
tags: ctf kringlecon-2021 web aws
intro: 
---

## Objective: Now Hiring!
> What is the secret access key for the Jack Frost Tower job applications server?

In this challenge, we're given an form page to exploit and the hint of AWS EC2.

![Application page](/images/kringlecon2021/hiring_1.png)

There's several fields we need to fill out but the one of interest is the URL since that brings to mind SSRF (server-side request forgery) attacks. In a nutshell, SSRF allows you to specify a URL in a webform that is then evaluated by the backend/internal server with the results being returned without any requirement for authentication. This vulnerability can leak sensitive information such as credentials or account secrets.

![Application page - URL field](/images/kringlecon2021/hiring_2.png)

It took some trial and error but I soon learned I had to use Burp Suite to be able to see the full response. Also, the `name` field had to be set to `secret` or `access` or I wouldn't get any response.

Based on the documentation for AWS metatdata access, my first URL to target was `http://169.254.169.254/latest/meta-data/iam/info` (or `http://[fd00:ec2::254]/latest/meta-data/iam/info` for IPv6) to pull all the available roles.

![Response #1](/images/kringlecon2021/hiring_3.png)

Then, based on the response, the next URL to get the actual secret was `http://169.254.169.254/latest/meta-data/iam/security-credentials/jf-deploy-role`.

![Response #2](/images/kringlecon2021/hiring_4.png)

To see my other writeups for this CTF, check out the tag [#kringlecon-2021](/tags#kringlecon-2021).

## References
- [SSRF Attack Definition](https://portswigger.net/web-security/ssrf)
- [AWS EC2 Metadata Retrieval](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html)
- [AWS EC2 Metadata Categories](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-categories.html)