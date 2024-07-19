import streamlit as st
import google.generativeai as genai
import os

# Function to set up Google Gemini AI
def setup_gemini_ai(api_key):
    genai.configure(api_key=api_key)
    return genai

# Streamlit app setup
st.title("Question Generator with Google Gemini AI")

# API Key input
api_key = st.text_input("Enter your Gemini API Key", type="password")

if api_key:
    try:
        # Initialize Google Gemini AI
        genai_client = setup_gemini_ai(api_key)
        
        # Set up the chat session
        chat_session = genai_client.start_chat()
        
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
                prompt = f"Generate 30 random questions and answers from the following text:\n{extracted_text}"
                response = chat_session.send_message(prompt)
                generated_text = response.text
                
                st.write("Generated Questions and Answers:")
                st.write(generated_text)
                
                # Generate and provide download link for PDF
                pdf_buffer = generate_pdf(generated_text.split('\n'))
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
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    import io

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
