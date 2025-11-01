import streamlit as st
import requests

st.set_page_config(page_title="Smart Student Assistant", layout="wide")
backend_url = st.text_input("Backend URL", value="http://localhost:8000")

st.title("🎓 Smart Student Assistant")

# Question Answering
st.header("🧠 Ask a Question from Text")
context = st.text_area("Enter text or notes here:")
question = st.text_input("Ask a question:")
if st.button("Get Answer"):
    r = requests.post(f"{backend_url}/qa", json={"context": context, "question": question})
    st.write("**Answer:**", r.json().get("answer"))

# Summarization
st.header("📚 Summarize Text")
summary_input = st.text_area("Paste text to summarize:")
if st.button("Summarize"):
    r = requests.post(f"{backend_url}/summarize", json={"text": summary_input})
    st.write("**Summary:**", r.json().get("summary"))

# Handwriting OCR
st.header("✍️ Handwriting to Text")
uploaded = st.file_uploader("Upload handwritten image", type=["png", "jpg", "jpeg"])
if uploaded:
    files = {"file": (uploaded.name, uploaded.getvalue())}
    r = requests.post(f"{backend_url}/hw-eval", files=files)
    st.write("**Extracted Text:**")
    st.code(r.json().get("extracted_text"), language="text")
