# Warning Behavior Analysis Toolkit (WBAT)

## Overview

The Warning Behavior Analysis Toolkit (WBAT) is a computational framework developed to measure the warning behaviors indicative of radicalization in online discourse. Specifically, we use the toolkit within the context of radical misogynist ideologies. WBAT leverages linguistic and behavioral analytics to identify shifts towards extremist ideologies. This toolkit primarily focuses on Reddit as a case study, analyzing interactions within Manosphere communities and their impact on users' adoption of radical views.

# Table 1: A summary of the warning behaviors, our methods for measuring them, and previous work which motivates their inclusion in our toolkit.

| Type               | Trait     | Definition                                 | Measure                                      | References                  |
| ------------------ | --------- | ------------------------------------------ | -------------------------------------------- | --------------------------- |
| **Language**       | Fixation  | Increased preoccupation with a topic.      | Frequency of occurrence of feminism keywords | [17, 33, 54, 67]            |
|                    | Grievance | Expression of real or perceived injustice. | Grievance keywords                           | [83], [19, 21, 53, 78, 79]  |
|                    | Power     | Increased need for power and authority.    | LIWC ‘Power’ keywords                        | [6, 15, 43, 77, 79]         |
| **Emotions**       | Anger     | Exhibition of anger and aggression.        | LIWC ‘Anger’ keywords                        | [6, 54, 65, 66, 79]         |
| **Outlook**        | Negative  | Negative outlook and sentiment.            | % of negative content (VADER)                | [6, 22, 80]                 |
|                    | Toxicity  | Increase in hate speech and toxicity.      | % of toxic content (Perspective)             | [23, 65, 66, 73]            |
| **Identification** | Ingroup   | Increased identification with a group.     | LIWC ‘We’ keywords                           | [9, 17, 21, 53, 54, 73, 79] |
|                    | Outgroup  | Increased mention of the outgroup.         | LIWC ‘They’ keywords                         | [9, 21, 65, 73, 76, 79]     |
## Measurements

The toolkit is structured around several Python scripts, each dedicated to a specific aspect of the analysis:

1. **Toxicity Analysis (`Toxicity.py`)**: Identifies and quantifies the presence of toxic language in user discourse.
2. **Fixation Detection (`fixation.py`)**: Measures users' fixation on specific topics, indicating potential radicalization cues. Topics keywords can be changed.
3. **Grievance Expression Analysis (`grievance.py`)**: Evaluates expressions of perceived injustices or grievances. This is an implementation of [83]
4. **Group Identification** (**`group_identification.py`**): Measures the user's out-group and in-group identification.
5. **Negativity Tracking (`negative.py`)**: Monitors negative sentiment and outlook in user communications.
## Reference

For more detailed theoretical underpinnings and empirical validation of the methodologies implemented in WBAT, please refer to the paper 
"Making a Radical Misogynist: How Online Social Engagement with the Manosphere Influences Traits of Radicalization" by Hussam Habib, Padmini Srinivasan, and Rishab Nithyanand.
### References for Table

Based on your request to include only the references mentioned in the Table 1 from the PDF document, with the original reference numbers, here's the list:

### References for Table 1

[6] Stephane J. Baele. 2017. "Lone-actor terrorists’ emotions and cognition: An evaluation beyond stereotypes." *Political Psychology*, 38(3), pp. 449–468.  
[9] JM Berger. 2017. "Extremist Construction of Identity: How Escalating Demands for Legitimacy Shape and Define In-Group and Out-Group Dynamics," ICCT Research Paper, April 2017.  
[15] Cindy K. Chung and James W. Pennebaker. 2011. "Using computerized text analysis to assess threatening communications and behavior." In *Threatening communications and behavior: Perspectives on the pursuit of public figures*, pp. 3–32.  
[17] Katie Cohen, Fredrik Johansson, Lisa Kaati, and Jonas Clausen Mork. 2014. "Detecting linguistic markers for radical violence in social media." *Terrorism and Political Violence*, 26(1), pp. 246–256.  
[19] Emily Corner, Paul Gill, Ronald Schouten, and Frank Farnham. 2018. "Mental disorders, personality traits, and grievance-fueled targeted violence: the evidence base and implications for research and practice." *Journal of personality assessment*, 100(5), pp. 459–470.  
[21] Bertjan Doosje, Annemarie Loseman, and Kees Van Den Bos. 2013. "Determinants of radicalization of Islamic youth in the Netherlands: Personal uncertainty, perceived injustice, and perceived group threat." *Journal of Social Issues*, 69(3), pp. 586–604.  
[22] Kevin S. Douglas, James R.P. Ogloff, Tonia L. Nicholls, and Isabel Grant. 1999. "Assessing risk for violence among psychiatric patients: the HCR-20 violence risk assessment scheme and the Psychopathy Checklist: Screening Version." *Journal of consulting and clinical psychology*, 67(6), pp. 917.  
[23] Vincent Egan, Jon Cole, Ben Cole, Laurence Alison, Emily Alison, Sara Waring, and Stamatis Elntib. 2016. "Can you identify violent extremists using a screening checklist and open-source intelligence alone?" *Journal of Threat Assessment and Management*, 3(1), pp. 21.  
[33] Ted Grover and Gloria Mark. 2019. "Detecting potential warning behaviors of ideological radicalization in an alt-right subreddit." In *Proceedings of the International AAAI Conference on Web and Social Media*, Vol. 13, pp. 193–204.  
[54] J Reid Meloy. 2018. "The operational development and empirical testing of the Terrorist Radicalization Assessment Protocol (TRAP–18)." *Journal of personality assessment*, 100(5), pp. 483–492.  
[65] D. Elaine Pressman and John Flockton. 2012. "Calibrating risk for violent political extremists and terrorists: The VERA 2 structured assessment." *The British Journal of Forensic Practice*.  
[67] J Reid Meloy, Jens Hoffmann, Angela Guldimann, and David James. 2012. "The role of warning behaviors in threat assessment: An exploration and suggested typology." *Behavioral sciences & the law*, 30(3), pp. 256–279.  
[77] Allison G. Smith. 2004. "From words to action: Exploring the relationship between a group’s value references and its likelihood of engaging in terrorism." *Studies in Conflict & Terrorism*, 27(5), pp. 409–437.  
[78] Allison G. Smith. 2018. "How radicalization to terrorism occurs in the United States: What research sponsored by the National Institute of Justice tells us." *US Department of Justice, Office of Justice Programs, National Institute of Justice*.  
[79] Allison G. Smith. 2018. "Risk factors and indicators associated with radicalization to terrorism in the United States: What research sponsored by the National Institute of Justice tells us." *US Department of Justice, Office of Justice Programs, National Institute of Justice*.  
[83] Isabelle van der Vegt, Maximilian Mozes, Bennett Kleinberg, and Paul Gill. 2021. "The Grievance Dictionary: understanding threatening language use." *Behavior research methods*.  
