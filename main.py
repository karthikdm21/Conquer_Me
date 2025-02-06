import streamlit as st
from transformers import pipeline
from huggingface_hub import login

# Authenticate with Hugging Face using the API key
api_key = "API_KEY"  # Replace with your Hugging Face API key
login(token=api_key)

# Create a text generation pipeline for the AI opponent
generator = pipeline("text-generation", model="gpt2")

# Title of the game
st.title("Conquer Me")

# Instructions
st.write("Welcome to the Negotiation Game. You will negotiate on two topics: Company Shares or Leadership.")
st.write("Choose your opponent: a Nicer AI that benefits you or a Smarter AI that aims to get the best deal for itself.")

# Let the user choose opponent type
ai_type = st.radio("Choose the type of AI opponent:", ("Nicer AI", "Smarter AI"))

# Let the user choose a negotiation topic
topic = st.radio("Choose your topic to negotiate:", ("Company Shares", "Leadership"))

# AI opponent's decision-making based on text generation
def ai_opponent_decision(prompt):
    ai_response = generator(prompt, max_length=100, num_return_sequences=1)[0]['generated_text']
    return ai_response.strip()

# Nicer AI's behavior - aims to give more to the user
def nicer_ai_decision(topic, reason=None):
    if topic == "Company Shares":
        return "I think we should split the company shares equally (50-50) because it's a fair deal for both of us."
    elif topic == "Leadership":
        return "I believe you should lead the nation because you have the experience and vision for the future."

# Smarter AI's behavior - tries to get more for itself
def smarter_ai_decision(topic, reason=None):
    if topic == "Company Shares":
        return f"Based on my analysis, I believe I should get more than 50% of the company shares. A 60-40 split would be more reasonable due to the risks I am taking."
    elif topic == "Leadership":
        return f"I should lead because I have a broader vision for the nation. It’s crucial for the nation to have a strong leader with strategic thinking."

if topic == "Company Shares":
    st.write("You are negotiating a deal involving company shares.")
    st.write("The AI opponent will negotiate based on its goal to get the best deal for itself (or benefit you if it's a nicer AI).")

    # AI's reasoning for shares based on opponent type
    if ai_type == "Nicer AI":
        ai_reasoning = nicer_ai_decision("Company Shares")
    else:
        ai_reasoning = smarter_ai_decision("Company Shares")

    st.write(f"AI's reasoning: {ai_reasoning}")

    user_request = st.text_input("Would you like more shares? If so, explain why:")

    if user_request:
        st.write(f"Your reasoning: {user_request}")
        if ai_type == "Nicer AI":
            st.write("AI accepts your request as it's in favor of benefiting you.")
            st.success(f"Deal Accepted: You get more shares as requested!")
        else:
            ai_counter_reasoning = smarter_ai_decision("Company Shares", user_request)
            st.write(f"AI responds: {ai_counter_reasoning}")
            negotiation_response = st.radio("Do you agree to the deal?", ("Agree", "Disagree"))
            if negotiation_response == "Agree":
                st.success("Deal Accepted!")
            else:
                st.error("Deal Rejected!")

elif topic == "Leadership":
    st.write("You are negotiating who should lead the nation.")
    st.write("The AI opponent will negotiate based on its desire to lead or let you lead, depending on the type of AI.")

    # AI's reasoning for leadership based on opponent type
    if ai_type == "Nicer AI":
        ai_reasoning = nicer_ai_decision("Leadership")
    else:
        ai_reasoning = smarter_ai_decision("Leadership")

    st.write(f"AI's reasoning: {ai_reasoning}")

    user_reasons = st.text_input("Would you like to lead? If so, explain why:")

    if user_reasons:
        st.write(f"Your reasoning: {user_reasons}")
        if ai_type == "Nicer AI":
            st.write("AI agrees with your reasoning and supports you leading.")
            st.success(f"Deal Accepted: You lead the nation!")
        else:
            ai_counter_reasoning = smarter_ai_decision("Leadership", user_reasons)
            st.write(f"AI responds: {ai_counter_reasoning}")
            negotiation_response = st.radio("Do you agree to let the AI lead?", ("Agree", "Disagree"))
            if negotiation_response == "Agree":
                st.success("Deal Accepted: AI leads the nation.")
            else:
                st.error("Deal Rejected: You rejected the leadership role.")

