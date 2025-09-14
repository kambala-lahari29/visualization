import streamlit as st
from pypdf import PdfReader
from docx import Document
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io

st.title("Text Extraction and Multi-Visualization App")

uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=['pdf', 'docx'])

if uploaded_file is not None:
    # Extract text from PDF
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    # Extract text from DOCX
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
            words_top, counts = zip(*most_common)

            # Bar chart for top 10 words
            plt.figure(figsize=(10,5))
            plt.bar(words_top, counts, color='skyblue')
            plt.xticks(rotation=45)
            plt.xlabel("Words")
            plt.ylabel("Frequency")
            plt.title("Top 10 Most Frequent Words")
            st.pyplot(plt)
            plt.clf()

            # Word Cloud
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
            plt.figure(figsize=(10,5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.title("Word Cloud")
            st.pyplot(plt)
            plt.clf()

            # Pie chart of word length categories
            short_words = sum(1 for w in words if len(w) <= 3)
            medium_words = sum(1 for w in words if 4 <= len(w) <= 7)
            long_words = sum(1 for w in words if len(w) > 7)

            labels = ['Short (<=3 chars)', 'Medium (4-7 chars)', 'Long (>7 chars)']
            sizes = [short_words, medium_words, long_words]

            plt.figure(figsize=(6,6))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['lightcoral', 'gold', 'lightskyblue'])
            plt.title('Word Length Distribution')
            st.pyplot(plt)

        else:
            st.info("No words found to visualize.")
    else:
        st.info("No text extracted from the document.")
