import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai

# 🔑 Paste your Gemini API key here
genai.configure(api_key="AIzaSyC56ORyxwrXZNlBZn-ki6E65Ab0-YJEBqE")

# 📌 Use the lighter flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# 📄 Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# ✂️ Limit input size to avoid quota issues
def limit_text(text, max_chars=3000):
    return text[:max_chars]

# 🌟 Streamlit UI
st.set_page_config(page_title="PolicyPal AI", layout="centered")
st.title("📄 PolicyPal AI - Insurance Assistant")

uploaded_file = st.file_uploader("Upload a Health Insurance PDF", type="pdf")

if uploaded_file is not None:
    st.success("✅ PDF uploaded successfully!")
    full_text = extract_text_from_pdf(uploaded_file)
    limited_text = limit_text(full_text)

    user_question = st.text_input("Ask a question about the policy:")

    if st.button("Ask"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(
                    f"Based on the following policy:\n{limited_text}\n\nAnswer this question: {user_question}"
                )
                st.write("💡 **Answer:**", response.text)
            except Exception as e:
                st.error(f"❌ Gemini Error:\n\n{str(e)}")
