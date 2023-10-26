# DETI STORE

#### Project 1 - SIO

---

## Index

1. [Introduction](#Introduction)

2. [Overview](#Overview)

3. [Vulnerabilites](#Vulnerabilites)

- CWE - 89
- CWE - 352
- CWE - 798
- CWE - 620
- CWE - 521
- CWE - 522
- CWE - 434

## 1. Introduction

The present report serves as documentation for Project 1 of SIO which intends to explore the possible vulnerabiilites, their consequences and their counters in a webapp for a ficitious online store: Deti Store.

---

## 2. Overview

To implement and counteract our selected vulnerabilites we used Flask: HTML with Boostrap on the frontend, data renderization with templating using Jinja2 and a SQLite database for data persistency on the backend.

## 3. Vulnerabilites

### CWE - 89 - Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')

### CVSS

##### Severity: 4.3

##### Vector String: CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N

##### Breakdown

| Metric | Value | Justification                                                                                                                                            |
| ------ | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AV     | N     | The vulnerability is exploitable from a remote network, such as the internet, without requiring user interaction.                                        |
| AC     | L     | The attack requires low complexity, such as the availability of an easily guessable or known SQL injection payload.                                      |
| PR     | N     | No privileges are required to exploit the vulnerability.                                                                                                 |
| UI     | N     | No user interaction is required to exploit the vulnerability.                                                                                            |
| S      | U     | The vulnerability affects the security of the entire system, not just individual resources within the system.                                            |
| C      | L     | The vulnerability may allow an attacker to access or modify sensitive information, but the data is typically difficult to recover or exploited.          |
| I      | L     | The vulnerability may allow an attacker to modify data, but it is unlikely to have a significant impact on the integrity of the affected system or data. |
| A      | N     | The vulnerability does not affect the availability of the affected system or data.                                                                       |

#### Abstract

An example of SQL injection is when an attacker inserts Structured Query Language (SQL) code into a Web form input box to access resources or modify data.

An SQL query is a request for a database action to be taken.

Normally, when a user enters their name and password into the corresponding text boxes on a Web form for user authentication, those values are added to a SELECT query.

The user is given access if the values they submitted are found as expected; if they are not, access is refused.

However, except for names and passwords, most Web forms don't have any safeguards in place to prevent input.

In the absence of such security measures, a hacker may utilize the input boxes to give the database their own request, allowing them to download the entire database or engage with it in other illegal ways.

In this way, SQL injection can give an attacker unrestricted access to sensitive data, such as client information, personally identifiable information, trade secrets, intellectual property, and other sensitive data.

The ability to read, edit, and steal confidential data enables attackers to easily gain access to and take over a system.

#### Exploitation

In this case, SQL injection is possible in the password field of the login page, by entering an input that abuses the SQL quotation notation, for example ' or 1=1 -- as such:

Video

#### Counteraction

Originally, the password is received and processed directly like so:

```python
query = text(
        "SELECT * FROM user WHERE username = '"
        + user
        + "' AND password = '"
        + key
        + "';"
    )

result = db.session.execute(query).fetchall()

if not result:
    flash("User not found!", "error")
    return redirect(url_for("auth.login"))

user = User.query.filter_by(username=user).first()
login_user(user)
```

To correct this, the **werkzeug** library was employed to process the password through hashing. Furthermore, **SQL Alchemy** was used to make sure that the password matches that which is associated with the user. In pratical terms, this translates into a guard clause like the following:

```python
user = User.query.filter_by(username=username).first()
if not user or not check_password_hash(user.password, key):
    flash("Please check your login details and try again.")
    return redirect(url_for("auth.login"))

login_user(user)
```

### CWE - 352 - Cross-Site Request Forgery

CVSS

##### Severity: 6.1

##### Vector String: CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N

##### Breakdown

| Metric | Value | Justification                                                                                                                                                                                                                                      |
| ------ | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AV     | N     | The vulnerability is exploitable from a remote network, such as the internet, without requiring direct access to the target system. An attacker can leverage the vulnerability by crafting a malicious website that is visited by the target user. |
| AC     | L     | The attack requires low complexity, such as the availability of a known CSRF payload or the ability to predict predictable input fields in the application.                                                                                        |
| PR     | N     | No privileges or special knowledge are required to exploit the vulnerability.                                                                                                                                                                      |
| UI     | R     | User interaction is required to exploit the vulnerability, such as visiting a malicious website or clicking a malicious link.                                                                                                                      |
| S      | C     | The vulnerability only affects the security of individual resources, such as a single user account, rather than the entire system.                                                                                                                 |
| C      | N     | The vulnerability does not allow an attacker to access sensitive information or steal user data.                                                                                                                                                   |
| I      | H     | The vulnerability allows an attacker to modify data, such as changing the target user's account settings or making unauthorized purchases.                                                                                                         |
| A      | N     | The vulnerability does not affect the availability of the affected system or data, but it still poses a serious security risk.                                                                                                                     |

#### Abstract

When a web server is constructed to receive a request from a client without any way for verifying that it was submitted intentionally, an attacker may be able to fool a client into sending an unintended request to the web server, which will be viewed as a genuine request.
This can be accomplished by a URL, image load, XMLHttpRequest, or other means, and can result in data exposure or inadvertent code execution.

To prevent CSRF attacks, web developers can implement measures such as using anti-CSRF tokens, rate-limiting requests, and same-site cookie policies.

#### Exploitation

For the purposes of this assignment, we chose to implement a fake, scam site, that would resemble the overall appearance of our real site, enough so that at least some more naïve users would fall for, as seen below:

![](https://media.discordapp.net/attachments/852109272262770710/1070352387778293882/image.png?width=1294&height=661)

In reality, it hides a malicious intent, implemented with the following hidden input, that is submitted when the user clicks the button:

```html
<form
  hidden
  id="hack"
  target="csrf-frame"
  action="http://127.0.0.1:5000/shop/add_to_cart/1"
  method="POST"
  autocomplete="off"
></form>

<iframe
  hidden
  name="csrf-frame"
  id="frame"
  width="1000px"
  height="1000px"
></iframe>
```

It appears to offer free checkups, but in reality, when clicked on, will make use of the user's stored cookies in order to inject a ficticious appointment in their account, as seen on the bottom of this user's appointment list:

Foto

Here's a dramatization of how this vulnerability could be exploited in a real world scenario, the user finds themselves on our scam site and wants their free checkup, so, logically, they click on the button in order to proceed. By doing this, when returning to the real eHealth Corp site, they are confronted with and alert injected by the attacker, alongside a new, ficticious appointment:

Foto

#### Counteraction

**Flask-WTF** is a popular library for creating web forms in Flask and it provides built-in protection against CSRF attacks by including an anti-CSRF token in each form rendered by the library.

When a form is generated, Flask-WTF adds a hidden field with a unique token to the HTML code. This token is then sent back to the server when the form is submitted. On the server, Flask-WTF checks the token against the stored value and only processes the form if the token is valid. This way, even if an attacker is able to trick a user into submitting a form, the attack will be rejected because the attacker does not have access to the valid anti-CSRF token.

This way, attackers can't submit anything without having they themselves access to the page where the data they intend to submit is meant to be submitted in.

In terms of implementing this fix, it's as simple as importing the aforementioned library and adding a hidden input as the one seen below:

```html
<form method="POST" action="/product/add_to_cart/{{ product.id }}">
  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
  <button class="btn btn-success" style="margin-right: 5px;">
    Add To Cart
  </button>
  {% with messages = get_flashed_messages() %} {% if messages %} {% for message
  in messages %}
  <div class="alert alert-danger" role="alert">{{ message }}</div>
  {% endfor %} {% endif %} {% endwith %}
</form>
```

### CWE - 798 - Use of Hard-coded Credentials

#### CVSS

##### Severity: 8.8

##### Vector String: CVSS:3.1/AV:A/AC:H/PR:H/UI:N/S:U/C:H/I:H/A:N

##### Breakdown

| Metric | Value | Justification                                                                                                                                                                                        |
| ------ | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AV     | A     | The vulnerability is exploitable from the local system and does not require access to a network. An attacker can leverage the vulnerability by directly accessing the vulnerable software or device. |
| AC     | H     | The attack requires high complexity, such as reverse engineering the software or having physical access to the device.                                                                               |
| PR     | H     | High privileges or special knowledge are required to exploit the vulnerability, such as access to the source code or administrator privileges.                                                       |
| UI     | N     | No user interaction is required to exploit the vulnerability.                                                                                                                                        |
| S      | U     | The vulnerability affects the security of the entire system, potentially exposing all user data or the integrity of the system.                                                                      |
| C      | H     | The vulnerability allows an attacker to access sensitive information or steal user data, such as usernames and passwords, potentially compromising the entire system.                                |
| I      | H     | The vulnerability allows an attacker to modify data, such as changing the target user's account settings or making unauthorized purchases.                                                           |
| A      | N     | The vulnerability does not affect the availability of the affected system or data, but it still poses a serious security risk.                                                                       |

#### Abstract

Hard-coded credentials generally leave a big gap that allows an attacker to bypass the authentication that the software administrator has configured.
This vulnerability may be difficult to discover for the system administrator.
Even if it is detected, it can be impossible to repair, thus the administrator may be obliged to disable the product completely.

In this project, the inbound variation of this vulnerability will be explored: this is where a default administrator account is generated and a basic password is hard-coded into the product and connected with that account.
This hard-coded password is the same for each installation of the product, and system administrators often cannot change or disable it without manually editing the application or otherwise updating the software.
If the password is ever found or publicized (which is often on the Internet), anyone with this password can access the product.
Lastly, because all installations of the program will use the same password, even across businesses, huge assaults such as worms are possible.

In order to address this security risk, it is important to avoid using hard-coded credentials in software development. Instead, administrators should be required to create unique and secure passwords for each installation of the product, and the product should be designed to store these credentials securely. This can help to prevent unauthorized access and minimize the potential damage from a security breach.
Additionally, regular security audits and testing can help to identify and address any hard-coded credentials that may be present in the product.

#### Exploitation

During development, several test users can be created and left, by accident, in the database tables , for example:

```
email: admin@admin.com

password: admin
```

#### Counteraction

One possible solution to this, and the one we chose to implement, is to develop a script that does a sanity check on the database that is exectuted on deploy, thereby ensuring that the product is deployed in a clean state.

Our implementation of this solution is as follows:

```python
def check_db_security(db):
    query = text("SELECT username FROM user WHERE isAdmin = True;")
    result = db.session.execute(query).fetchall()
    usernames = [username[0] for username in result]

    for username in usernames:
        query = text("SELECT * FROM user WHERE username = '" + username + "';")
        result = db.session.execute(query).fetchall()

        print("User " + username + " found!")
        query = text("DELETE FROM user WHERE username = '" + username + "';")
        db.session.execute(query)
        db.session.commit()
        print("Deleted user: " + username)
        print("-------------------")
```

Forcing users to change their password on first use is a security measure that can help to mitigate the risk posed by hard-coded credentials in software systems. This approach works by requiring new users to create a unique and secure password immediately after their first successful login. By doing this, the hard-coded credentials are effectively nullified, as the attacker would need to know the newly created password in order to gain access to the product.

This type of password policy helps to ensure that new users start using secure passwords right away, reducing the risk of unauthorized access. In addition, forcing password changes on a regular basis can help to maintain the security of the system over time. By implementing this type of security measure, organizations can help to protect their data and systems from potential security breaches caused by hard-coded credentials.

### CWE - 620 - Unverified Password Change

#### CVSS

##### Severity: 8.1

##### Vector String: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N

##### Breakdown

| Metric | Value | Justification                                                                                                                                                                                                                             |
| ------ | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AV     | N     | The vulnerability is exploitable from a remote network, such as the internet, without requiring direct access to the target system. An attacker can leverage the vulnerability by exploiting a weakness in the password change mechanism. |
| AC     | L     | The attack requires low complexity, such as exploiting a known vulnerability in the password change mechanism or guessing a user's password reset token.                                                                                  |
| PR     | N     | No privileges or special knowledge are required to exploit the vulnerability.                                                                                                                                                             |
| UI     | N     | No user interaction is required to exploit the vulnerability.                                                                                                                                                                             |
| S      | U     | The vulnerability affects the security of the entire system, potentially exposing all user data or the integrity of the system.                                                                                                           |
| C      | H     | The vulnerability allows an attacker to access sensitive information or steal user data, such as changing the target user's password and compromising their account.                                                                      |
| I      | H     | The vulnerability allows an attacker to modify data, such as changing the target user's account settings or making unauthorized purchases.                                                                                                |
| A      | N     | The vulnerability does not affect the availability of the affected system or data, but it still poses a serious security risk.                                                                                                            |

#### Abstract

The product does not need knowledge of the original password or the usage of another type of authentication when creating a new password for a user.

An attacker might use this to change passwords for another account, acquiring the rights associated with that user.

#### Exploitation

By not asking for the user's current password when editing their profile, this allows a rogue agent who has access to the user's current session to lock them out of their account:

Foto

#### Counteraction

Simply adding a field that requires the user to input their current password ensures their account isn't currently compromised:

Foto

### CWE - 521 - Weak Password Requirements

#### CVSS

##### Severity: 7.5

##### Vector String: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N

##### Breakdown

| Metric | Value | Justification                                                                                                                                                                                                                                                        |
| ------ | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AV     | N     | The vulnerability is exploitable from a remote network, such as the internet, without requiring direct access to the target system. An attacker can leverage the vulnerability by exploiting the weak password requirements and guessing or cracking weak passwords. |
| AC     | L     | The attack requires low complexity, such as exploiting a known vulnerability in the password requirements or guessing a user's password.                                                                                                                             |
| PR     | N     | No privileges or special knowledge are required to exploit the vulnerability.                                                                                                                                                                                        |
| UI     | N     | No user interaction is required to exploit the vulnerability.                                                                                                                                                                                                        |
| S      | U     | The vulnerability affects the security of the entire system, potentially exposing all user data or the integrity of the system.                                                                                                                                      |
| C      | H     | The vulnerability allows an attacker to access sensitive information or steal user data, such as compromising the target user's account.                                                                                                                             |
| I      | H     | The vulnerability allows an attacker to modify data, such as changing the target user's account settings or making unauthorized purchases.                                                                                                                           |
| A      | N     | The vulnerability does not affect the availability of the affected system or data, but it still poses a serious security risk.                                                                                                                                       |

#### Abstract

To provide an assertion of identity for a system user, authentication systems frequently rely on a memorized secret (also known as a password).
As a result, it is critical that this password be sufficiently complex and difficult for an attacker to guess.
The particular criteria for how complicated a password must be vary according to the type of system being secured.
Choosing the right password requirements and enforcing them via implementation are important to the authentication mechanism's overall success.

#### Exploitation

The exploitation of this vulnerability simply surrounds the fact that a simple password is itself simple to crack, and therefore dangerous to be allowed.

#### Counteraction

By simply forbidding users from using weak passwords, we counteract this weakness

We do this by refusing to accept passwords that consist of simple or predictable sequences like being shorter than 8 characters in length, not having a digit, not having mixcased letters or a special symbol, using the following `ìf` statements:

```python
if len(key) < 8:
    flash("A senha deve ter pelo menos 8 caracteres")
    return redirect(url_for("register.regist"))
elif not any(char.isdigit() for char in key):
    flash("A senha deve ter pelo menos um número")
    return redirect(url_for("register.regist"))
elif not any(char.isupper() for char in key):
    flash("A senha deve ter pelo menos uma letra maiúscula")
    return redirect(url_for("register.regist"))
elif not any(char.islower() for char in key):
    flash("A senha deve ter pelo menos uma letra minúscula")
    return redirect(url_for("register.regist"))
elif not any(char in "~`! @#$%^&*()_-+={[}]|\:;\"'<,>.?/" for char in key):
    flash("A senha deve ter pelo menos um caractere especial")
    return redirect(url_for("register.regist"))
```

### CWE - 522 - Insufficiently Protected Credentials

#### CVSS

##### Severity: 7.5

##### Vector String: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N

##### Breakdown

| Metric | Value | Justification                                                                                                                                                                                                                                                                                                                        |
| ------ | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| AV     | N     | The vulnerability is exploitable from a remote network, such as the internet, without requiring direct access to the target system. An attacker can leverage the vulnerability by exploiting insufficient protection of the target system's credentials, such as stealing clear-text passwords or unencrypted authentication tokens. |
| AC     | L     | The attack requires low complexity, such as exploiting a known vulnerability in the credential storage mechanism or accessing unsecured data storage.                                                                                                                                                                                |
| PR     | N     | No privileges or special knowledge are required to exploit the vulnerability.                                                                                                                                                                                                                                                        |
| UI     | N     | No user interaction is required to exploit the vulnerability.                                                                                                                                                                                                                                                                        |
| S      | U     | The vulnerability affects the security of the entire system, potentially exposing all user data or the integrity of the system.                                                                                                                                                                                                      |
| C      | H     | The vulnerability allows an attacker to access sensitive information or steal user data, such as compromising the target user's account.                                                                                                                                                                                             |
| I      | H     | The vulnerability allows an attacker to modify data, such as changing the target user's account settings or making unauthorized purchases.                                                                                                                                                                                           |
| A      | N     | The vulnerability does not affect the availability of the affected system or data, but it still poses a serious security risk.                                                                                                                                                                                                       |

#### Abstract

The site sends or saves authentication credentials, but it does so in an unsafe manner that enables for unwanted monitoring and/or extraction.

#### Exploitation

When editing the user profile, one can simply change the field in the URL corresponding to the user's ID to an ID of another user that exists, accessing, henceforth this user's profile editing page.

Video

#### Counteraction

As previously referenced, the URL contains a field relative to the user's ID, this is because the current user's ID is passed as an argument in the routing system, as such:

```python
@profile.route("/profile/<int:id>", methods=["GET"])
@login_required
def changeProfile(id):
```

To counteract this, this page's URL has its ID field dropped and this argument is omitted, not being taken in consideration any longer, making it impossible for a given user to access any other editing page that would be able to alter third party data, like so:

```python
@profile.route("/edit_profile", methods=["GET"])
@login_required
def changeProfile():
```

### CWE-434 - Unrestricted Upload of File with Dangerous Type

#### CVSS

##### Severity: 7.5

##### Vector String: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N

##### Breakdown

| Metric | Value | Justification                                                                                                                                                                                                                                                                                    |
| ------ | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| AV     | N     | The vulnerability is exploitable from a remote network, such as the internet, without requiring direct access to the target system. An attacker can leverage the vulnerability by uploading a file with a dangerous type, such as a script or executable, and executing it on the target system. |
| AC     | L     | The attack requires low complexity, such as uploading a file to an unprotected endpoint or exploiting a misconfigured file type validation mechanism.                                                                                                                                            |
| PR     | N     | No privileges or special knowledge are required to exploit the vulnerability.                                                                                                                                                                                                                    |
| UI     | N     | No user interaction is required to exploit the vulnerability.                                                                                                                                                                                                                                    |
| S      | U     | The vulnerability affects the security of the entire system, potentially exposing all user data or the integrity of the system.                                                                                                                                                                  |
| C      | H     | The vulnerability allows an attacker to execute arbitrary code, such as downloading malware or compromising the target system.                                                                                                                                                                   |
| I      | H     | The vulnerability allows an attacker to modify data, such as modifying system files or inserting malicious code.                                                                                                                                                                                 |
| A      | N     | The vulnerability does not affect the availability of the affected system or data, but it still poses a serious security risk.                                                                                                                                                                   |

#### Abstract

The software enables the upload or transfer of risky file types that can be automatically processed within the environment of the product.

#### Exploitation

When editing the user's profile the site allows for the uploading of a file, intended only to be of the PNG or JPEG file type. This condition is left to the user's good will, which means a bad actor could upload a dangerous file type that could jeopardize the normal workflow of the application.

In the following example, the user inputs a JPG type file and the system, predictably, accepts it.

Video

#### Counteraction

To counter this, we used a simple guard clause to impede an upload of any other file type that isn't PNG/JPEG:

```python
if profile_picture.filename.endswith(
    ".png"
) or profile_picture.filename.endswith(".jpeg"):
    try:
        profile_picture.save(
            os.path.join("static/images", profile_picture.filename)
        )
        new_user = User(
            username=user,
            password=generate_password_hash(key),
            name=nome,
            email=email,
            phone=phone,
            image=profile_picture.filename,
            security_question=security_question,
        )
    except:
        flash("Erro ao fazer upload da imagem!", category="danger")
        return redirect(url_for("register.regist"))
else:
    flash(
        "Por favor insira uma imagem com extensão .png ou .jpeg",
        category="danger",
    )
    return redirect(url_for("register.regist"))
```

This is the system's behaviour after this change:

Video

---

## 4. Final Considerations

Besides the aforementioned attack vectors, we tried to implement and combat CWE-1336, commonly known as 'Template Injection' but this was counteracted in a previous version of Jinja2.

This project heavily contributed to our awareness of the necessity of developing apps and services with a focus on security, highlighting the risks of not doing so.

### Total CVSS Severity Score: 65
