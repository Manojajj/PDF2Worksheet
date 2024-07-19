import streamlit as st
import google.generativeai as genai
import os
import io
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to configure and use Google Gemini AI
def generate_questions_with_gemini(api_key, text, num_questions=30):
    genai.configure(api_key=api_key)
    
    # Create a prompt for the API
    prompt = f"Generate {num_questions} random questions and answers from the following text:\n{text}"
    
    # Call the API to generate text
    response = genai.generate_text(
        prompt=prompt,
        model="gemini-1.0-pro",  # Adjust this model name as per the available models
        temperature=1,
        top_p=0.95
    )
    
    # Process and return the response text
    generated_text = response.get("text", "")  # Adjust based on actual API response format
    return generated_text.split('\n')

# Streamlit app setup
st.title("Question Generator with Google Gemini AI")

# API Key input
api_key = st.text_input("Enter your Gemini API Key", type="password")

if api_key:
    # File upload
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_file:
        # Extract text from PDF
        pdf_reader = PdfReader(uploaded_file)
        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text()
        
        st.text_area("Extracted Text", extracted_text, height=300)
        
        if st.button("Generate Worksheet"):
            # Generate questions and answers
            try:
                qa_pairs = generate_questions_with_gemini(api_key, extracted_text, num_questions=30)
                
                st.write("Generated Questions and Answers:")
                for i, text in enumerate(qa_pairs):
                    st.write(f"**Question {i+1}:** {text}")
                
                # Generate and provide download link for PDF
                pdf_buffer = generate_pdf(qa_pairs)
                st.download_button(
                    label="Download as PDF",
                    data=pdf_buffer,
                    file_name="questions_and_answers.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Function to generate PDF
def generate_pdf(qa_pairs):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica", 12)
    c.drawString(30, height - 30, "Generated Questions and Answers")
    
    y = height - 50
    for i, text in enumerate(qa_pairs):
        c.drawString(30, y, f"Question {i+1}: {text}")
        y -= 20
        c.drawString(30, y, f"Answer: [Generated Answer Here]")
        y -= 40
        if y < 40:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 30

    c.save()
    buffer.seek(0)
    return buffer
