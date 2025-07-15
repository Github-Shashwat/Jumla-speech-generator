from langchain.prompts import PromptTemplate

# Speech Generation Template
SPEECH_TEMPLATE = """
Write a satirical Indian political rally speech in Hinglish about the topic: "{topic}".

Parameters:
- Tone: {tone}/10 (1=Secular, 10=Nationalistic)
- Blame Target: {blame}
- Freebies Level: {freebies}/10 (1=None, 10=Maximum)
- Hindutva Intensity: {hindutva}/10 (1=Minimal, 10=Maximum)
- Development Promises: {development}/10 (1=Vague, 10=Specific)

Guidelines:
- Use classic political phrases like "Mitron", "Sabka Saath Sabka Vikas", "Desh ki janta maaf nahi karegi"
- Mix Hindi and English naturally (Hinglish)
- Include typical rally elements: crowd interactions, dramatic pauses, rhetorical questions
- Make it humorous and ironic while maintaining the satirical tone
- Length: 200-300 words
- Include some popular political catchphrases and slogans

Speech:
"""

# Critique Template
CRITIQUE_TEMPLATE = """
Analyze the following satirical political speech and provide a humorous critique:

Speech: {speech}

Provide analysis on:
1. Jumla Density (how many empty promises per paragraph)
2. Blame-Shifting Score (how effectively blame is redirected)
3. Crowd Manipulation Tactics used
4. Realism Score (how close to actual political rhetoric)
5. Hinglish Authenticity
6. Overall Satirical Effectiveness

Format as a witty, sarcastic review with ratings out of 10 for each category.
Keep the tone light and humorous while being insightful.

Critique:
"""

# Topic Summarization Template
TOPIC_SUMMARIZER_TEMPLATE = """
Summarize the following news headlines into 5 distinct trending topics suitable for political speeches:

Headlines:
{headlines}

Extract the main themes and present them as:
1. Topic Name
2. Topic Name
3. Topic Name
4. Topic Name
5. Topic Name

Keep topics broad enough for political commentary but specific enough to be meaningful.
"""

# Create prompt templates
speech_prompt = PromptTemplate(
    input_variables=["topic", "tone", "blame", "freebies", "hindutva", "development"],
    template=SPEECH_TEMPLATE
)

critique_prompt = PromptTemplate(
    input_variables=["speech"],
    template=CRITIQUE_TEMPLATE
)

topic_summarizer_prompt = PromptTemplate(
    input_variables=["headlines"],
    template=TOPIC_SUMMARIZER_TEMPLATE
)