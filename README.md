# 
# 🎯Jumla-speech-generator: Satirical Campaign Speech Simulator

An LLM + LangChain powered app that crafts Hinglish satirical speeches about today's trending topics, with sliders to control tone, blame, freebies & more — complete with witty AI critique.

---

## 🚀 Features

* **Real-time Trending Topics**: Fetches latest news from Google News RSS
* **Customizable Speech Parameters**: Control tone, blame targets, freebies, and more
* **Hinglish Generation**: Authentic mix of Hindi and English political rhetoric
* **AI Critique System**: Analyzes speeches for "jumla density" and effectiveness
* **Multiple LLM Providers**: Groq (Llama3-70B) and OpenAI (GPT-3.5-Turbo)
* **Speech History**: Track and review generated speeches
* **Downloadable Speeches**: Save speeches as text files

---

## 🛠️ Quick Setup Instructions

### 🗂️ 0. Clone the repository

```bash
git clone https://github.com/yourusername/satirical-speech-simulator.git
cd satirical-speech-simulator
```

### 📦 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 🔑 2. Set up API keys

```bash
cp .env.template .env
```

Edit the `.env` file and add your API keys:

```
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 🧪 3. Test your setup (optional)

Run a quick test script to verify API connectivity and chains:

```bash
python quick_start.py
```

### 🚀 4. Launch the app

Start the Streamlit app:

```bash
streamlit run app.py
```

---

## 🎮 Usage

### API Setup

* Choose LLM provider (Groq or OpenAI) and enter API key.

### Topic Selection

* Click "Refresh Topics" to fetch latest headlines and pick one, or enter a custom topic.

### Parameter Configuration

* Adjust sliders for tone, blame, freebies, hindutva, and development.

### Speech Generation

* Click “Generate Satirical Speech” — view speech + AI critique, and download if needed.

---

## 🏗️ Project Structure

```
satirical_speech_simulator/
├── app.py
├── chains.py
├── prompts.py
├── news_fetcher.py
├── requirements.txt
├── quick_start.py
├── .env.template
└── .streamlit/
    └── config.toml
```

---

## 📊 Speech Parameters

* **Tone (1–10)**: Secular → Nationalistic
* **Blame Target**: Opposition, Previous Govt, Media, etc.
* **Freebies Level (1–10)**: Minimal → Extensive
* **Hindutva Intensity (1–10)**: Low → High
* **Development Promises (1–10)**: Vague → Specific

---

## 🎭 Sample Output

**Generated Speech:**

```
Mitron! Hamari sarkar ne sabko vikas diya, aur opposition sirf jumlebaazi karti hai. Digital India ke through humne corruption ko khatam kiya hai...
```

**AI Critique:**

```
Jumla Density: 8/10 — excellent vagueness and blame-shifting.
```

---

## 🔧 Configuration

* Groq: [https://console.groq.com/](https://console.groq.com/)
* OpenAI: [https://platform.openai.com/](https://platform.openai.com/)
* Google News RSS (India edition)

---

## 🔮 Future Enhancements

* Regional language support
* Speech-to-text for audio input
* Shareable speech cards
* Voice synthesis playback
* User authentication & saved speeches

---

## ⚠️ Disclaimer

This is a satirical tool created for entertainment and educational purposes only. It parodies political rhetoric and is not intended for real campaigns or misinformation.

---

Made with ❤️ for satire & tech.


