import streamlit as st
import requests

st.set_page_config(page_title="Smart Student Assistant", layout="wide")
st.title("🎓 Smart Student Assistant")

backend_url = st.text_input("Backend URL", value="http://localhost:8000")

st.markdown("## 🧠 Ask a question from your notes")
context = st.text_area("Enter context / notes here", height=200)
question = st.text_input("Ask a question about the above text")
if st.button("Get Answer"):
    if not backend_url:
        st.error("Set backend URL first")
    else:
        try:
            r = requests.post(f"{backend_url}/qa", json={"context": context, "question": question}, timeout=15)
            st.success("Answer:")
            st.write(r.json().get("answer"))
        except Exception as e:
            st.error(f"Request failed: {e}")

st.markdown("---")
st.markdown("## 📚 Summarize text")
summary_input = st.text_area("Paste text to summarize", height=150)
if st.button("Summarize Text"):
    if not backend_url:
        st.error("Set backend URL first")
    else:
        try:
            r = requests.post(f"{backend_url}/summarize", json={"text": summary_input}, timeout=20)
            st.success("Summary:")
            st.write(r.json().get("summary"))
        except Exception as e:
            st.error(f"Request failed: {e}")

st.markdown("---")
st.markdown("## ✍️ Handwriting OCR")
uploaded = st.file_uploader("Upload a handwritten image (png/jpg/jpeg)", type=["png", "jpg", "jpeg"])
if uploaded:
    if st.button("Extract Text from Image"):
        if not backend_url:
            st.error("Set backend URL first")
        else:
            try:
                files = {"file": (uploaded.name, uploaded.getvalue())}
                r = requests.post(f"{backend_url}/hw-eval", files=files, timeout=30)
                st.success("Extracted Text:")
                st.code(r.json().get("extracted_text"))
            except Exception as e:
                st.error(f"Request failed: {e}")
