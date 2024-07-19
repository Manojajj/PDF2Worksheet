import streamlit as st
import google.generativeai as genai

# Streamlit app setup
st.title("Gemini AI Chatbot")

# Text input for API key
api_key = st.text_input("Enter your Gemini API Key", type="password")

# Text input for the prompt
user_input = st.text_area("Enter your message")

if st.button("Generate Response"):
    if api_key and user_input:
        # Configure the Gemini API
        genai.configure(api_key=api_key)

        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
        )

        # Start chat session
        chat_session = model.start_chat(history=[])

        # Send message and get response
        response = chat_session.send_message(user_input)

        # Display response
        st.write("Response:")
        st.write(response.text)
    else:
        st.warning("Please enter both API key and message.")
