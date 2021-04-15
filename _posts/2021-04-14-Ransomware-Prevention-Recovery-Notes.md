---
layout: default
title: "Ransomware Thoughts"
date: 2021-04-14 13:00:00 -0000
---

# Ransomware Thoughts

With ransomware being an ever-present threat, I thought I'd jot down some best practices I've come across to prevent and, if the worst should happen, recover from such an attack. This is far from a comprehensive list but can be a jumping-off point when developing a new plan or updating existing processes and procedures.

## Vulnerability Management & Patching

The famous and infamous WannaCry ransomware a few years ago was made possible by an SMB vulnerability in Windows OS dating back to XP. A patch to fix this issue was available about X months before the first WannaCry infection was announced but many organization had not updated and were victims of the malware.

Keeping your systems up to date is critical to preventing ransomware and infections in general. However, the number of vulnerabilities and patches released can be overwhelming. This requires a vulnerability management program that prioritizes patching and mitigation efforts based on two factors: criticality and likelihood.

Criticality is a measurement of what would happen if the system or application went down. This could be measured in cost of production loss, cost of manpower required to fix the issue, or something else.

For likelihood, this could be measured by how easy the system and/or application can be altered or affected. This may depend on the network configurations, system hardening, and change management procedures.

A vulnerability management program can be as simple or as complex as an organization chooses to define it. However, it must have measurable performance indicators and carry the weight to drive change.

## Everyone Shares & SMB

A common way for ransomware to spread through a network is using the SMBv1 protocol and unsecure shares. Be sure SMBv1 is disabled (this can be done via GPO) and unsecure shares are locked down to only those who need access (also known as principal of least privilege).

To take this a step further, an audit process can and should also be implemented to ensure the insecure protocol and share permissions are configured properly. It does no good if the environment is set up correctly only to fall back into bad habits when not monitored.

## Endpoint Protection

A key first line of defense is Endpoint Detection and Response (EDR) software. These tools monitor behavior on endpoints and can detect suspicious/malicious activity without solely relying on static indicators of compromise (IOCs) such as hashes, IPs, and domains. Depending on the specific product, this software can detect and prevent known malicious binaries as well as common malicious behaviors to identify new or unknown malware strains that are not yet documented.

When implementing an EDR solution, it's best to have a plan on how to manage the tool - this is _not_ a set-and-forget product that can run in the background without any monitoring or fine-tuning.

## Email Filtering

One of the most common vehicles of ransomware is email. To prevent end users from clicking on malicious links or opening suspicious attachments, consider implementing an email filter. Email filtering can include quarantining/blocking any messages with high-risk attachments (e.g. EXE, JS, RAR, etc.), rewriting external links to enable malicious URL tracking, tagging incoming email as external and high risk, scanning emails and attachments against known IOCs, and blocking known bad domains/email addresses.

## Backups

In the worst case scenario that ransomware spreads across the network, backups are an absolute necessity. However, just making backups isn't enough. You'll need to also test backups regularly and keep them offline when not in use. A good place to start is the 3-2-1 rule described by [CISA](https://us-cert.cisa.gov/sites/default/files/publications/data_backup_options.pdf). There isn't a one-size fits all approach to backups and sometimes there are constraints due to technology, budget, manpower, etc. However, preserving a known-good copy of critical data and configurations will make recovering from a ransomware attack much less painful.

## Incident Response Plan

Last but certainly not least comes the incident response (IR) plan. When ransomware is detected on the network, it's a best practice to have a plan in place that is reviewed, tested, and updated regularly. Some items to consider when creating an IR plan are:

* Apart from IT/Cybersecurity, who should be involved and what responsibilities should they have?
* What tools do you currently have that can be used to respond? Who has the access and knowledge to use these tools effectively?
* Are there plans to call bring in external resources to assist if the issue is severe?
* What documentation steps are to be taken during and after an incident?

Similar to a vulnerability management program mentioned earlier, an IR plan can be as simple or complex as needed. I've seen them run the gamut of "call person X if something bad happens" to full-fledged responsibilities matrices for different types of incidents.

## Further Reading
* [Red Canary | How to choose an EDR](https://redcanary.com/blog/evaluating-edr-security-products/)
* [CISA | 1-2-3 Backup Rule](https://us-cert.cisa.gov/sites/default/files/publications/data_backup_options.pdf)
* [Infocyte | Incident Response Planning](https://www.infocyte.com/blog/2019/11/07/incident-response-planning-a-checklist-for-building-your-cyber-security-incident-response-plan/)
* [Amazon.com | Book on Incident Response & Computer Forensics](https://www.amazon.com/Incident-Response-Computer-Forensics-Third/dp/0071798684/ref=asc_df_0071798684/?tag=hyprod-20&linkCode=df0&hvadid=312091457223&hvpos=&hvnetw=g&hvrand=8943101042194686727&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9023473&hvtargid=pla-464897074962&psc=1&tag=&ref=&adgrpid=62820903995&hvpone=&hvptwo=&hvadid=312091457223&hvpos=&hvnetw=g&hvrand=8943101042194686727&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9023473&hvtargid=pla-464897074962)