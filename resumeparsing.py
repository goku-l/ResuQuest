import fitz
import re
import docx2txt
import os

filename = "C:\\Users\\gokul\\Downloads\\resumes\\gokul-resume.pdf"


def parse(text):
    for match in re.finditer(r"(\b\d{12}\b)", text):
        formatted_number = match.group()[0:2] + "-" + match.group()[2:]
        text = text.replace(match.group(), formatted_number)
    for match in re.finditer(r"(\b\d{11}\b)", text):
        formatted_number = match.group()[0:1] + "-" + match.group()[1:]
        text = text.replace(match.group(), formatted_number)

    phno = re.findall(
        r"(91|0|\+91|\(\+91\))?[-\s]?\b(\d{3}|\d{4})[-\s]?(\d{3})[-\s]?(\d{4}|\d{3})\b",
        text,
    )
    #     phno = re.findall(
    #     r"(91|0|\+91|\(\+91\))?[-\s]?\b(\d{4})[-\s]?(\d{3})[-\s]?(\d{3})\b",
    #     text,
    # )

    phno = (",".join("".join(x[1:]) for x in phno)).split(",")

    email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)

    linkedin = re.search(r"linkedin\.com\/in\/[a-zA-Z0-9_-]+", text)
    github = re.search(r"github\.com\/[a-zA-Z0-9_-]+", text)
    if linkedin:
        linkedin = linkedin.group()
    else:
        linkedin = ""

    if github:
        github = github.group()
    else:
        github = ""

    if len(phno) == 0:
        phno = ""
    else:
        phno = phno[0]

    if len(email) == 0:
        email = ""
    else:
        email = email[0]
    i = 0
    name = ""
    while i < len(email):
        if email[i] == "@":
            break
        if email[i].isalpha():
            name += email[i]
        i += 1
    text = {
        "name": name,
        "phno": phno,
        "email": email,
        "linkedin": linkedin,
        "github": github,
    }
    return text


parse(filename)
