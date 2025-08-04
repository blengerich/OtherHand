import streamlit as st
from openai import OpenAI
import requests

MAX_EMAIL_LENGTH = 254

# Set page config
st.set_page_config(page_title="OtherHand AI", layout="centered")

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 1.1rem !important;
    }
    .stTextInput > div > input {
        font-size: 1.1rem !important;
    }
    .stTextArea textarea {
        font-size: 1.1rem !important;
    }
    .stChatMessageContent {
        font-size: 1.15rem !important;
        line-height: 1.6;
    }
    .chat-container {
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 1.2rem;
        background-color: #fafafa;
        margin-bottom: 2rem;
    }

    .stChatMessageContent {
        font-size: 1.1rem !important;
        line-height: 1.6;
    }
    .stTextInput>div>input {
        font-size: 1.05rem !important;
        padding: 0.5rem;
    }

    .chat-input {
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🖐 OtherHand AI")
st.markdown(
    """
    Ever feel like ChatGPT just takes your side?

    **OtherHand** flips the script — it reconstructs the *other person’s perspective* and gives a thoughtful, neutral response.
    """
)




# Input API key
api_key = st.text_input("🔑 Your OpenAI API Key (retrieve yours [here](https://platform.openai.com/settings/profile/api-keys))", type="password")
#st.caption("🛡️ Using a public device? [Revoke your key](https://platform.openai.com/account/api-keys) after you're done.")

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

if api_key:
    client = OpenAI(api_key=api_key)

    # Main chat container
    chat_container = st.container()

    # Input box container — rendered below the chat
    input_container = st.container()

    # Render past messages (above input)
    with chat_container:
        for msg in st.session_state.messages[1:]:  # skip system message
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Render input (at bottom)
    with input_container:
        user_input = st.chat_input("Write a message...")

    # Handle input and model response
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages,
                max_tokens=800,
                temperature=0.7
            )
            reply = response.choices[0].message.content.strip()
            st.session_state.messages.append({"role": "assistant", "content": reply})

            with chat_container:
                with st.chat_message("assistant"):
                    st.markdown(reply)

        except Exception as e:
            st.error(f"Error: {e}")

        #st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Please enter your OpenAI API key to start the conversation.")

    with st.expander("Want to use OtherHand without an API key?", expanded=False):
        st.markdown("OtherHand is just a wrapper on ChatGPT right now. "
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

# Disclaimer section
with st.sidebar:
    st.markdown("### OtherHand AI")
    with st.expander("🔍 Disclaimers & Safety Notes", expanded=False):
        st.markdown(
            """
            - This tool is experimental and not a substitute for therapy, legal advice, or crisis support.
            - All responses are generated by an AI model and may contain errors or inappropriate assumptions.
            - Use your best judgment and always consult qualified professionals for serious personal, emotional, or medical situations.
            - If you are in crisis, consider reaching out to a licensed therapist, a medical professional, or a trusted support hotline.
            - We do **not** store your data or your OpenAI key. Your session is temporary and local to your browser.
            - 🛡 If you are using a public or shared device, [revoke your key](https://platform.openai.com/account/api-keys) after use.
            """
        )

if len(st.session_state.messages) > 2:
    with st.expander("📬 Want a full version?", expanded=False):
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