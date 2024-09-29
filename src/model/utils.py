import os
import openai
import google.generativeai as genai

# Standard OpenAI API
standard_keys = os.environ.get("OPENAI_API_KEY").split(":")

# Replicate API
os.environ["REPLICATE_API_TOKEN"] = os.environ.get("REPLICATE_API_TOKEN")

# Gemini API
genai.configure(api_key=os.environ.get("GEMINI_KEY"))

# Iterative count bound
iterative_count_bound = 3
