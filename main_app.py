import streamlit as st
from chains import SpeechGenerator, ModelManager
from news_fetcher import NewsFetcher
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="🎯 Satirical Campaign Speech Simulator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #FF6B35, #F7931E);
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .speech-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #FF6B35;
        margin: 1rem 0;
    }
    
    .critique-container {
        background: #fff3cd;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #F7931E;
        margin: 1rem 0;
    }
    
    .slider-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 Satirical Campaign Speech Simulator</h1>
    <p>LLM + LangChain powered app that crafts Hinglish satirical speeches about today's trending topics</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'speech_history' not in st.session_state:
    st.session_state.speech_history = []
if 'news_fetcher' not in st.session_state:
    st.session_state.news_fetcher = NewsFetcher()

# Sidebar
with st.sidebar:
    st.header("🛠️ Configuration")
    
    # Model Selection
    st.subheader("🤖 Model Settings")
    providers = ModelManager.get_available_providers()
    selected_provider_name = st.selectbox(
        "Choose LLM Provider",
        options=list(providers.keys()),
        index=0
    )
    selected_provider = providers[selected_provider_name]
    
    # API Key Input
    api_key_name = ModelManager.get_api_key_name(selected_provider)
    api_key = st.text_input(
        f"Enter {api_key_name}",
        type="password",
        help=f"Get your API key from the {selected_provider_name} dashboard"
    )
    
    # Validate API key
    api_key_valid = ModelManager.validate_api_key(api_key, selected_provider)
    if api_key and not api_key_valid:
        st.error("Invalid API key format!")
    
    st.divider()
    
    # Topic Selection
    st.subheader("📰 Topic Selection")
    
    # Refresh topics button
    if st.button("🔄 Refresh Topics", use_container_width=True):
        with st.spinner("Fetching latest news..."):
            st.session_state.topics = st.session_state.news_fetcher.get_trending_topics()
            st.success("Topics refreshed!")
    
    # Initialize topics if not exists
    if 'topics' not in st.session_state:
        with st.spinner("Loading trending topics..."):
            st.session_state.topics = st.session_state.news_fetcher.get_trending_topics()
    
    # Topic selector
    selected_topic = st.selectbox(
        "Select Topic",
        options=st.session_state.topics,
        index=0
    )
    
    # Custom topic input
    custom_topic = st.text_input("Or enter custom topic:")
    final_topic = custom_topic if custom_topic else selected_topic
    
    st.divider()
    
    # Speech Parameters
    st.subheader("🎛️ Speech Parameters")
    
    with st.container():
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        tone = st.slider(
            "**Tone**",
            min_value=1,
            max_value=10,
            value=7,
            help="1=Secular, 10=Nationalistic"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        blame_options = ["Opposition", "Previous Government", "Foreign Forces", "Media", "Corrupt Officials", "System"]
        blame = st.selectbox("**Blame Target**", blame_options, index=0)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        freebies = st.slider(
            "**Freebies Level**",
            min_value=1,
            max_value=10,
            value=6,
            help="1=None, 10=Maximum"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        hindutva = st.slider(
            "**Hindutva Intensity**",
            min_value=1,
            max_value=10,
            value=4,
            help="1=Minimal, 10=Maximum"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        development = st.slider(
            "**Development Promises**",
            min_value=1,
            max_value=10,
            value=8,
            help="1=Vague, 10=Specific"
        )
        st.markdown('</div>', unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎤 Generate Speech")
    
    # Generate button
    if st.button("🚀 Generate Satirical Speech", use_container_width=True, type="primary"):
        if not api_key_valid:
            st.error("Please enter a valid API key in the sidebar!")
        else:
            try:
                with st.spinner("Generating satirical speech..."):
                    # Initialize speech generator
                    speech_gen = SpeechGenerator(api_key, selected_provider)
                    
                    # Generate speech and critique
                    result = speech_gen.generate_speech_and_critique(
                        topic=final_topic,
                        tone=tone,
                        blame=blame,
                        freebies=freebies,
                        hindutva=hindutva,
                        development=development
                    )
                    
                    # Store in session state
                    st.session_state.current_speech = result["speech"]
                    st.session_state.current_critique = result["critique"]
                    
                    # Add to history
                    st.session_state.speech_history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "topic": final_topic,
                        "speech": result["speech"],
                        "critique": result["critique"],
                        "parameters": {
                            "tone": tone,
                            "blame": blame,
                            "freebies": freebies,
                            "hindutva": hindutva,
                            "development": development
                        }
                    })
                    
                    st.success("Speech generated successfully!")
                    
            except Exception as e:
                st.error(f"Error: {e}")
    
    # Display current speech
    if 'current_speech' in st.session_state:
        st.markdown(f"""
        <div class="speech-container">
            <h3>🎙️ Generated Speech</h3>
            <p style="font-size: 1.1em; line-height: 1.6;">{st.session_state.current_speech}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Download button
        speech_text = f"Topic: {final_topic}\n\nSpeech:\n{st.session_state.current_speech}"
        st.download_button(
            label="📥 Download Speech",
            data=speech_text,
            file_name=f"satirical_speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    
    # Display critique
    if 'current_critique' in st.session_state:
        st.markdown(f"""
        <div class="critique-container">
            <h3>🔍 AI Critique</h3>
            <p style="font-size: 1.05em; line-height: 1.6;">{st.session_state.current_critique}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.header("📊 Current Settings")
    
    # Display current parameters
    st.markdown(f"""
    **Topic:** {final_topic}
    
    **Parameters:**
    - 🎯 Tone: {tone}/10
    - 🎯 Blame: {blame}
    - 🎯 Freebies: {freebies}/10
    - 🎯 Hindutva: {hindutva}/10
    - 🎯 Development: {development}/10
    """)
    
    st.divider()
    
    # Speech History
    st.subheader("📜 Speech History")
    
    if st.session_state.speech_history:
        for i, entry in enumerate(reversed(st.session_state.speech_history[-5:])):  # Show last 5
            with st.expander(f"🕐 {entry['timestamp']} - {entry['topic'][:30]}..."):
                st.write(f"**Topic:** {entry['topic']}")
                st.write(f"**Speech:** {entry['speech'][:200]}...")
                st.write(f"**Parameters:** Tone={entry['parameters']['tone']}, Blame={entry['parameters']['blame']}")
    else:
        st.info("No speeches generated yet. Generate your first speech!")
    
    # Clear history button
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.speech_history = []
        st.success("History cleared!")

# Footer
st.markdown("""
<div class="footer">
    <p>🎯 Satirical Campaign Speech Simulator | Built with Streamlit + LangChain</p>
    <p>⚠️ This is a satirical tool for entertainment purposes only</p>
</div>
""", unsafe_allow_html=True)

# Instructions
with st.expander("ℹ️ How to Use"):
    st.markdown("""
    1. **Setup**: Enter your API key for either Groq or OpenAI in the sidebar
    2. **Choose Topic**: Select from trending topics or enter a custom topic
    3. **Adjust Parameters**: Use the sliders to control speech characteristics
    4. **Generate**: Click the generate button to create your satirical speech
    5. **Review**: Read the generated speech and AI critique
    6. **Download**: Save your speech as a text file
    
    **Parameter Guide:**
    - **Tone**: Controls how nationalistic vs secular the speech sounds
    - **Blame Target**: Who gets blamed for problems
    - **Freebies**: How many free schemes are promised
    - **Hindutva Intensity**: Religious rhetoric level
    - **Development Promises**: How specific the development promises are
    """)

# Debug info (only show in development)
if st.checkbox("🔧 Debug Info"):
    st.write("Session State Keys:", list(st.session_state.keys()))
    st.write("API Key Valid:", api_key_valid)
    st.write("Selected Provider:", selected_provider)