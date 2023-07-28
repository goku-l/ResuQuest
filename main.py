import streamlit as st
import os
from joblib import load
import fitz
import docx2txt
import nltk
import re
import string
import sys
import resumeparsing
from sklearn.preprocessing import LabelEncoder
from github import Github
import requests
import shutil
import pandas as pd
import webbrowser
from urllib.parse import quote

stopwords = nltk.corpus.stopwords.words("english")
random_forest = load("random_forest_classifier_model.joblib")
word_vectorizer = load("resume_vectorizer.joblib")
labelencoder = load("label_encoder.joblib")


def open_file(file_path):
    webbrowser.open(file_path)


def clean_text(text):
    # convert text to lowercase
    text = text.lower()
    # remove any numeric characters
    text = "".join([word for word in text if not word.isdigit()])

    #     text = [word for word in text if re.search("\d", word)== None]
    # remove URLs
    text = re.sub("http\S+\s*", " ", text)
    # remove RT and cc
    text = re.sub("RT|cc", " ", text)
    # remove hashtags
    text = re.sub("#\S+", "", text)
    # remove mentions
    text = re.sub("@\S+", "  ", text)
    # punctuations removal
    text = "".join([word for word in text if word not in string.punctuation])
    text = re.sub("\W", " ", str(text))
    # stopwords removal
    text = [word for word in text.split() if word not in stopwords]
    # replace consecutive non-ASCII characters with a space
    text = re.sub(r"[^\x00-\x7f]", r" ", str(text))
    # extra whitespace removal
    text = re.sub("\s+", " ", text)
    return text


def classify():
    folder_path = "D:\\ResuQuest\\temporary"
    files = os.listdir(folder_path)
    l = {}
    for file_name in files:
        result = {
            "Name": "",
            "Phno": "",
            "email": "",
            "LinkedIn": "",
            "GitHub": "",
            "File": "",
        }

        filename = os.path.join(folder_path, file_name)
        result["File"] = filename
        data = ""
        if ".pdf" in filename:
            with fitz.open(filename) as doc:
                for page in doc:
                    data += page.get_text()
        else:
            data = docx2txt.process(filename)
        temp = resumeparsing.parse(data)
        result["Name"] = temp["name"].capitalize()
        result["Phno"] = temp["phno"]
        result["email"] = temp["email"]
        result["LinkedIn"] = temp["linkedin"]
        result["GitHub"] = temp["github"]
        data = clean_text(data)
        features = word_vectorizer.transform([data])

        predicted_label_random_forest = random_forest.predict(features)
        predicted_category_random_forest = labelencoder.inverse_transform(
            predicted_label_random_forest
        )
        access_token = "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"
        g = Github(access_token)
        username = result["GitHub"][11:]
        if username == "":
            result["GitHub Rating"] = 0
        else:
            try:
                user = g.get_user(username)
                followers_weight = 0.7
                repositories_weight = 0.3
                followers = user.followers
                repositories = user.public_repos

                result["GitHub Rating"] = round(
                    (repositories * repositories_weight)
                    + (followers * followers_weight),
                    2,
                )
            except Exception as e:
                result["GitHub Rating"] = 0
        if predicted_category_random_forest[0] in l:
            l[predicted_category_random_forest[0]].append(result)
        else:
            l[predicted_category_random_forest[0]] = []
            l[predicted_category_random_forest[0]].append(result)
    keys = l.keys()
    for x in keys:
        sorted_list = sorted(l[x], key=lambda x: x["GitHub Rating"], reverse=True)
        l[x] = sorted_list
        df = pd.DataFrame(sorted_list)
        df.index += 1
        df.at[1, "Name"] = "\u2728" + df.at[1, "Name"]
        df_styled = df.copy()
        df_styled["File"] = df_styled["File"].apply(
            lambda x: f'<a href="file:///{x}" style="color: inherit; text-decoration: none;">{x[23:]}</a>'
        )
        df_styled["GitHub"] = df_styled["GitHub"].apply(
            lambda x: f'<a href="https://{x}"  style="color: inherit; text-decoration: none;">{x[11:]}</a>'
        )
        df_styled["LinkedIn"] = df_styled["LinkedIn"].apply(
            lambda x: f'<a href="https://{x}" style="color: inherit; text-decoration: none;">{x[16:]}</a>'
        )
        df_styled["email"] = df_styled["email"].apply(
            lambda x: f'<a href="mailto:{x}" style="color: inherit; text-decoration: none;">{x}</a>'
        )
        html_table = df_styled.to_html(escape=False, index=False)
        st.write(
            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        )
        st.write(
            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        )
        st.write(
            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        )
        st.write(
            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        )
        # st.write(x)
        content = x
        colorname = (255, 247, 0)
        colored_text = f'<span style="color:rgb{colorname}">{content}</span>'

        st.markdown(colored_text, unsafe_allow_html=True)

        st.markdown(html_table, unsafe_allow_html=True)


# Function to save the uploaded files
def save_uploaded_file(file, upload_dir):
    file_path = os.path.join(upload_dir, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return file_path


def next_page():
    upload_dir = "D:\\ResuQuest\\temporary"

    # Ensure that the directory exists, create it if necessary
    os.makedirs(upload_dir, exist_ok=True)

    # Streamlit app code
    uploaded_files = st.file_uploader(
        "Upload PDF, DOC, or DOCX files",
        accept_multiple_files=True,
        type=["pdf", "doc", "docx"],
    )

    if uploaded_files:
        uploaded_filenames = []
        for file in uploaded_files:
            if (
                file.type == "application/pdf"
                or file.type == "application/msword"
                or file.type
                == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ):
                file_path = save_uploaded_file(file, upload_dir)
                uploaded_filenames.append(file.name)
            else:
                st.warning(f"Invalid file format: {file.name}")

        if uploaded_filenames:
            st.success("Files uploaded successfully")
            classify()


def welcome_page():
    # Centered page content
    st.title("ResuQuest")
    st.write("The Quest for the Ultimate Hire Starts Here")

    if st.button("Continue"):
        st.session_state["page"] = "next"


def main():
    st.session_state.setdefault(
        "page", "welcome"
    )  # Set the default page to the welcoming page

    if st.session_state["page"] == "welcome":
        welcome_page()
    elif st.session_state["page"] == "next":
        next_page()


if __name__ == "__main__":
    main()
