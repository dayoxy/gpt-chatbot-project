import os
import torch
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer

# Ensure required libraries are installed
try:
    import transformers
except ImportError:
    os.system("pip install transformers")
    import transformers

# Define model name (Change based on resources and preference)
MODEL_NAME = "gpt2"  # Examples: "facebook/opt-1.3b", "EleutherAI/gpt-neo-1.3B"

# Load tokenizer and model with error handling
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

def generate_text(prompt, max_length=50, temperature=0.7, top_p=0.9):
    """
    Generates text response using the GPT model.
    - max_length: Controls response length
    - temperature: Controls randomness (higher = more creative, lower = more deterministic)
    - top_p: Controls diversity (higher = more diverse responses)
    """
    inputs = tokenizer(prompt, return_tensors="pt")
    try:
        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=max_length,
            temperature=temperature,
            top_p=top_p,
            do_sample=True
        )
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        return f"Error generating response: {e}"

# Streamlit Chatbot Interface
def chatbot_interface():
    """
    Creates a simple chatbot interface using Streamlit.
    """
    st.title("Chatbot Interface")
    st.write("Powered by GPT-2")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    user_input = st.text_input("You:", "")
    if st.button("Send") and user_input.strip():
        response = generate_text(user_input, max_length=100, temperature=0.8)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Chatbot", response))
    
    st.subheader("Chat History")
    for sender, message in st.session_state.chat_history:
        st.write(f"**{sender}:** {message}")

if __name__ == "__main__":
    chatbot_interface()
