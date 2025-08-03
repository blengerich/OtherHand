import streamlit as st
from openai import OpenAI
import requests

# Set page config
st.set_page_config(page_title="OtherHand AI", layout="centered")

# Title and description
st.title("🖐 OtherHand AI")
st.markdown(
    """
    Ever feel like ChatGPT just takes your side?

    **OtherHand** flips the script — it reconstructs the *other person’s perspective* and gives a thoughtful, neutral response.

    _You'll need your own OpenAI API key. You can [get yours here](https://platform.openai.com/settings/profile/api-keys). It’s only used in your browser and never stored._
    """
)

# Input API key
api_key = st.text_input("🔑 Your OpenAI API Key", type="password")
st.caption("🛡️ Using a public device? [Revoke your key](https://platform.openai.com/account/api-keys) after you're done.")

# Session state setup
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """You're a neutral and insightful interpreter of human conflict and motivation. 
            First, reconstruct the other person's likely thoughts and feelings.
            Then, help the user move forward by reflecting on that reconstruction honestly.
            Do not avoid difficult truths. 
            If you need to make assumptions, be clear about them.
            Be emotionally intelligent but not biased. Avoid platitudes or moralizing.
            Be honest, even if it's uncomfortable. If you make assumptions, be clear. 
            If context is missing, ask a thoughtful follow-up question."""
        }
    ]

# Display conversation history
for msg in st.session_state.messages[1:]:  # skip system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if api_key:
    user_input = st.chat_input("Write a message...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages,
                max_tokens=800,
                temperature=0.7
            )
            reply = response.choices[0].message.content.strip()
            st.session_state.messages.append({"role": "assistant", "content": reply})

            with st.chat_message("assistant"):
                st.markdown(reply)

        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("Please enter your OpenAI API key to start the conversation.")


MAX_EMAIL_LENGTH = 254

with st.expander("📬 Want a full version? (Click to sign up)", expanded=False):
    st.markdown("This is just a wrapper on ChatGPT right now. "
                "We could build a version with no API key, saved sessions, and smarter back-and-forth conversation.")
    st.markdown("Want it? Drop your email and we’ll let you know when it’s live:")

    with st.form("interest_form"):
        email = st.text_input("Your email")
        submitted = st.form_submit_button("Notify Me")

        if submitted:
            if not email or "@" not in email or "." not in email:
                st.error("Please enter a valid email address.")
            elif len(email) > MAX_EMAIL_LENGTH:
                st.error(f"Email too long. Please use an email under {MAX_EMAIL_LENGTH} characters.")

            try:
                res = requests.post(
                    "https://formspree.io/f/myzpdovp",  # your Formspree endpoint
                    data={"email": email},
                    headers={"Accept": "application/json"}
                )
                if res.status_code == 200:
                    st.success("Thanks! We'll keep you in the loop.")
                else:
                    st.error("Something went wrong. Please try again later.")
            except Exception as e:
                st.error(f"Error: {e}")