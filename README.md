# SecurityRisks App

SecurityRisks App is a project for course [Cyber Security Base](https://cybersecuritybase.mooc.fi/) by University of Helsinki and MOOC.fi. The app illustrates 5 security issues from [OWASP top 10 list](https://owasp.org/www-project-top-ten/), so the code is flawed on purpose. 

## Flaws
 
### 1. Risk: Identification and Authentication Failures 
[Link](https://github.com/ruuskal/securityrisks-csb-project/blob/53b4aed6d46efa74109915a8e8da56f14c558338/polls/views.py#L90) 

Identification and authentication failure means that user’s identification or authentication is inadequate. When this happens the identities of the web applications’ users cannot be trusted, even if they are logged in as authenticated users. In our Securityrisks app this risk occurs because all kinds of passwords, even weak ones, are accepted in sign in form. Acceptance of weak passwords is problematic, because it opens a door for malicious entities to use brute force or simply guess the correct password. After the attacker has found a legitimate user’s password, there is no way to separate the attacker from a legitimate user.  

There should be more checks in the Securityrisks app to verify that the user chooses a strong password. For example, only passwords that are at least 10 characters long, do not contain the chosen username and that are not something obvious, like ‘password’, could be accepted. A natural solution would be to use Django’s signup sheet, that checks all the above. Using multi-factor authentication is also becoming more popular and should be implemented whenever an application deals with sensitive data.
 
### 2. Risk: Security Misconfiguration 
[Link](https://github.com/ruuskal/securityrisks-csb-project/blob/53b4aed6d46efa74109915a8e8da56f14c558338/securityrisks/settings.py#L52) 

Security misconfiguration can occur in many ways. Application may reveal too much information of its’ users or functionalities, that an attacker may take advantage of. (In Securityrisks app user is notified if the desired username is already taken in the sign in form, which can be seen as revealing too much information, although this is disputed.) Security misconfiguration may also happen when the application lacks configurations to prevent common attacks. Securityrisks app is vulnerable to clickjacking. In clickjacking attacker creates their own, invisible button on top of the real button, that is visible to the user. User then unintentionally clicks the attacker’s button, even though they intended to click some Securityrisks app’s button, like ‘vote’.  

Django’s X-Frame-Options is commented out in the settings. When it is in use, every outgoing HttpResponse is denied by default. This means, that attacker’s fake requests get denied by our app, because they come from another origin. Django also reminds that X-Frame-Options only work in modern browsers, so that would also have to be considered, when designing or using a web application. 

### 3. Risk: Broken Access Control 
[Link](https://github.com/ruuskal/securityrisks-csb-project/blob/53b4aed6d46efa74109915a8e8da56f14c558338/polls/views.py#L106) 

With broken access control users have access to information that they should not have access to. Broken access control means that users technically act within their rights, but the application does not perform enough checks to detect that the user is trying to do something they do not have the right to do. With identification and authentication failure (risk 1) an attacker has to impersonate someone else, but with broken access control, the attacker does not have to gain extra rights (such as admin rights) to execute their malicious act. Users may access the out-of-limits data even by mistake if the application does not predict all the ways users communicate with it. This is the case with our Securityrisks app. Page poll/pollusers.html contains all usernames and information of users’ last login. This page should only be accessed by admin, but there are no checks, if user simply types in the url /polls/pollusers.

The solution is to add some kind of verification for method `def pollusers()`, like commented out in [line 105](https://github.com/ruuskal/securityrisks-csb-project/blob/53b4aed6d46efa74109915a8e8da56f14c558338/polls/views.py#L105). It might also be wise to only use Django’s admin-site for seeing information of the pollusers, since it is implemented and accessible for the admin in the admin-site. Creating extra sites with sensitive information increases the possibility of broken access control failure.

### 4. Risk: Injection
[Link](https://github.com/ruuskal/securityrisks-csb-project/blob/53b4aed6d46efa74109915a8e8da56f14c558338/polls/views.py#L56)

Injection might happen when user input is not sanitized properly. An attacker might give input, which database handles as a new query and performs that query. This way the attacker might access some extra information from the database, or they might modify the database. In Securityrisks app users can create a new question for the poll. The question is saved to SQL-table ‘Question’ and the input text is directly saved to the database without any sanitation.

Solution is to not pass user input directly as it is. A more secure way is to omit the string formatting with quotes (`%s`) and use params instead. Another way is to create a question-object with Django’s syntax as shown in the commented-out in [lines 53-55](https://github.com/ruuskal/securityrisks-csb-project/blob/53b4aed6d46efa74109915a8e8da56f14c558338/polls/views.py#L52). In both ways SQL knows to escape the input data, so it cannot be interpreted as a query, even if it is written as one.

### 5. Risk: CSRF
[Link](https://github.com/ruuskal/securityrisks-csb-project/blob/53b4aed6d46efa74109915a8e8da56f14c558338/securityrisks/settings.py#L49) 

The Securityrisks app does not properly deal with cross-site request forgery. In an app, that has a CSRF vulnerability, legitimate users’ POST-requests might get hijacked by an attacker. The attacker forges the requests, that the user sends. The app does not suspect the malicious nature of these requests, because the user is properly authenticated in the app. The attacker’s goal might be to obtain or manipulate the app’s data, e.g., to manipulate legitimate user’s password. 

CSRF token is designed to prevent CSRF-attacks. The token has a unique value per session that the server knows and expects, but that the attacker won’t know or guess, making forging a request impossible. Django has a CSRF middleware, that is activated by default in the settings. Right now, the feature is foolishly commented out. We should use the feature and add `{% csrf_token %}` inside every form, as it is in [polls/signup.html](https://github.com/ruuskal/securityrisks-csb-project/blob/53b4aed6d46efa74109915a8e8da56f14c558338/polls/templates/polls/signup.html#L4).
