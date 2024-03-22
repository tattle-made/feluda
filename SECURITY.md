# Security Policy


Tattle takes the security and data privacy of our systems very seriously. Please read this document before performing any security analysis or reporting a vulnerability.


### Reporting Security Issues
Tattle encourages independent security researchers to responsibly disclose any vulnerabilities found in our site or applications.

- If you believe you have found a vulnerability or wish to report a security incident, you may send an email to 'admin@tattle.co.in'.
- If you have a Github account, you may also privately report a security vulnerability as an issue if enabled for the specific product (https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability).
- For the Feluda project, you may privately report the vulnerability here - https://github.com/tattle-made/feluda/security

Please add as much detail as possible in the report, including reproducible steps, to prevent delays in addressing the issue. Please test against the latest product version.

Tattle does not participate in a bug bounty program. However, we are happy to publicly acknowledge your contributions if we are made aware of the issue for the first time.

Tattle will make a best effort attempt to respond within 3 working days of receiving the report.


### Tattle's Vulnerability Disclosure Policy
Tattle will disclose vulnerabilities on a 90-day disclosure deadline with the following exceptions -

- If the deadline falls on a weekend or an Indian public holiday, the deadline will be moved to the next working day.
- If a high or critical severity vulnerability is discovered in a 3rd party product or dependency, we will inform the vendor and attempt to get the vulnerability fixed. We will delay the disclosure if a patch is scheduled for release within 14 days after the 90-day deadline.
- If we discover a "0day" vulnerability (an actively exploited, and previously unknown and unpatched vulnerability), we will disclose it within 7 days to prevent further compromise of machines and/or accounts. This is an unreasonable amount of time to release a well-tested fix, but allows sufficient time to publish advice and/or potential mitigations.


### Rules of Engagement, Testing, and Proof-of-Concepts

- Tattle products are open-source. You are encouraged to install standalone products locally for researching vulnerabilities.
- If you want to conduct penetration testing on any of Tattle's domains or subdomains, you will need an explicit written permission. During the process, you should coordinate with the Tattle team more closely to avoid escalation.
- Do not publicly post a proof-of-concept until the report is disclosed.
- You are required to follow Tattle's [Code of Conduct](https://github.com/tattle-made/feluda/blob/main/CODE_OF_CONDUCT.md) and [POSH Policy](https://drive.google.com/file/d/1AVr-xi85le6g-OY2DgEwa26aeMMs_d5o/view) when communicating with any team member.


### Out of scope

- Automated scanning of any kind
- Accessing or modifying data of other users
- Attacks on physical security
- Person-in-the-Middle attacks
- Social engineering of any kind
- Denial of Service
- Use of leaked credentials


### Safe Harbor
We follow this safe harbor policy for researchers

- https://github.com/Hacker0x01/docs.hackerone.com/blob/master/docs/organizations/safe-harbor-statement.md


### References
This policy has taken inspiration from the following sources:

- https://about.google/appsecurity/
- https://googleprojectzero.blogspot.com/2020/01/policy-and-disclosure-2020-edition.html
- https://about.gitlab.com/security/disclosure/
- https://hackerone.com/gitlab?type=team
- https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html
- https://www.hackerone.com/disclosure-guidelines
- https://docs.hackerone.com/organizations/safe-harbor-faq.html
- https://docs.hackerone.com/organizations/safe-harbor-statement.html

**First Release**: 22 March, 2024
