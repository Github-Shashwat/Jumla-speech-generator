from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import BaseOutputParser  # ✅ correct


from prompts import speech_prompt, critique_prompt, topic_summarizer_prompt
import streamlit as st
import os
from typing import Optional, Dict, Any

class SpeechGenerator:
    def __init__(self, api_key: str, model_provider: str = "groq"):
        self.api_key = api_key
        self.model_provider = model_provider
        self.llm = self._initialize_llm()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
    def _initialize_llm(self):
         if self.model_provider == "groq":
            return ChatGroq(
            api_key=self.api_key,  # Changed from groq_api_key
            model="llama3-70b-8192",  # Changed from model_name
            temperature=0.8
        )
         elif self.model_provider == "openai":
             return ChatOpenAI(
            api_key=self.api_key,  # Changed from openai_api_key
            model="gpt-3.5-turbo",  # Changed from model_name
            temperature=0.8
        )
    def generate_speech(self, topic: str, tone: int, blame: str, freebies: int, 
                   hindutva: int, development: int) -> str:
        try:
            speech_chain = LLMChain(
                 llm=self.llm,
                prompt=speech_prompt,
                output_key="speech"
        )
        
            result = speech_chain.invoke({  # Use invoke instead of run
                "topic": topic,
                "tone": tone,
                "blame": blame,
                "freebies": freebies,
                "hindutva": hindutva,
                "development": development
        })
        
            return result["speech"]
        except Exception as e:
         st.error(f"Error generating speech: {e}")
        return "Error generating speech. Please try again."
    

    def critique_speech(self, speech: str) -> str:
        """Generate critique of the speech"""
        try:
            critique_chain = LLMChain(
                llm=self.llm,
                prompt=critique_prompt,
                output_key="critique"
            )
            
            result = critique_chain.invoke({"speech": speech})
            return result["critique"]
        except Exception as e:
            st.error(f"Error generating critique: {e}")
            return "Error generating critique. Please try again."
    
# Better error handling for API calls
    def generate_speech_and_critique(self, topic: str, tone: int, blame: str, 
                                freebies: int, hindutva: int, development: int) -> Dict[str, str]:
        try:
            # Add timeout and retry logic
            speech_chain = LLMChain(
                llm=self.llm,
                prompt=speech_prompt,
                output_key="speech"
            )
            
            critique_chain = LLMChain(
                llm=self.llm,
                prompt=critique_prompt,
                output_key="critique"
            )
            
            # Sequential execution with error handling
            speech_result = speech_chain.invoke({
                "topic": topic,
                "tone": tone,
                "blame": blame,
                "freebies": freebies,
                "hindutva": hindutva,
                "development": development
            })
            
            critique_result = critique_chain.invoke({
                "speech": speech_result["speech"]
            })
            
            return {
                "speech": speech_result["speech"],
                "critique": critique_result["critique"]
            }
            
        except Exception as e:
            st.error(f"Error in chain execution: {e}")
            return {
                "speech": "Error generating speech. Please check your API key and try again.",
                "critique": "Error generating critique. Please try again."
            }
    def summarize_topics(self, headlines: str) -> str:
        """Summarize news headlines into topics"""
        try:
            topic_chain = LLMChain(
                llm=self.llm,
                prompt=topic_summarizer_prompt,
                output_key="topics"
            )
            
            result = topic_chain.invoke({"headlines": headlines})
            return result["topics"]
        except Exception as e:
            st.error(f"Error summarizing topics: {e}")
            return ""

class ModelManager:
    """Utility class to manage different model providers"""
    
    @staticmethod
    def get_available_providers() -> Dict[str, str]:
        return {
            "Groq (Llama3-70B)": "groq",
            "OpenAI (GPT-3.5-Turbo)": "openai"
        }
    
    @staticmethod
    def get_api_key_name(provider: str) -> str:
        key_mapping = {
            "groq": "GROQ_API_KEY",
            "openai": "OPENAI_API_KEY"
        }
        return key_mapping.get(provider, "API_KEY")
    
    @staticmethod
    def validate_api_key(api_key: str, provider: str) -> bool:
        """Basic validation for API key format"""
        if not api_key:
            return False
        
        if provider == "groq":
            return api_key.startswith("gsk_")
        elif provider == "openai":
            return api_key.startswith("sk-")
        
        return True