import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="📝",
    layout="centered"
)

st.title("📝 AI Content Assistant")
st.write("Generate tailored social media posts, captions, and hashtags instantly.")

# Sidebar API Key input
api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

# Form inputs
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        content_type = st.selectbox(
            "Content Type",
            ["Post", "Article", "Announcement", "Educational", "Promotional"]
        )
        platform = st.selectbox(
            "Platform",
            ["LinkedIn", "Instagram", "Twitter / X", "Facebook", "Blog"]
        )
        tone = st.selectbox(
            "Tone",
            ["Professional", "Casual", "Engaging", "Informative", "Humorous", "Persuasive"]
        )

    with col2:
        topic = st.text_input("Topic", placeholder="e.g., AI in Healthcare")
        target_audience = st.text_input("Target Audience", placeholder="e.g., Tech Enthusiasts, Founders")

    submit_button = st.form_submit_button("Generate Content")

# Logic execution
if submit_button:
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not topic or not target_audience:
        st.warning("Please fill in both Topic and Target Audience fields.")
    else:
        try:
            client = Groq(api_key=api_key)

            prompt = f"""
            You are an expert social media content creator.
            Create a complete post based on the following specifications:

            - Content Type: {content_type}
            - Platform: {platform}
            - Topic: {topic}
            - Target Audience: {target_audience}
            - Tone: {tone}

            Structure the response clearly as follows:
            1. **Main Post / Body**: Optimized for {platform} with appropriate formatting and emojis.
            2. **Caption / Summary**: Short, catchy summary or call-to-action.
            3. **Hashtags**: 5 to 10 relevant hashtags tailored to {platform}.
            """

            with st.spinner("Generating your content..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )

                st.success("Generated Content:")
                st.markdown(response.choices[0].message.content)

        except Exception as e:
            st.error(f"An error occurred: {e}")
