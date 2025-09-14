import streamlit as st
from pypdf import PdfReader
from docx import Document
from collections import Counter
import matplotlib.pyplot as plt

st.title("Text Extraction and Visualization App")

uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=['pdf', 'docx'])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        st.error("Unsupported file type")
        text = ""

    if text:
        st.subheader("Extracted Text")
        st.text_area("Text", text, height=300)

        words = text.split()
        if words:
            word_freq = Counter(words)
            most_common = word_freq.most_common(10)
            words, counts = zip(*most_common)

            plt.figure(figsize=(10,5))
            plt.bar(words, counts, color='skyblue')
            plt.xticks(rotation=45)
            plt.xlabel("Words")
            plt.ylabel("Frequency")
            plt.title("Top 10 Most Frequent Words")
            st.pyplot(plt)
        else:
            st.info("No words found to visualize.")
    else:
        st.info("No text extracted from the document.")
