import io
import requests
import streamlit as st
from openai import OpenAI
from huggingface_hub import InferenceClient

st.set_page_config(page_title"AI Mastermind Hub", page_icon="🤖",layout="centered")

try:
    GROQ_API_KEY= "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"
    HF_API_KEY=" "
except Exception:
    st.error(
        "API keys are missing!!"
        "add GROQ_API_KEY and HF_API_KEY"
    )
    st.stop()
groq_client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)
hf_client = InferenceClient(
    provider="auto",
    api_key=HF_API_KEY
)
MODEL = "openai/gpt-oss-20b"

IMAGE_MODELS ={
    "SDXL Base": "stabilityai/stable-diffusion-xl-base-1.0"
}
FILTER_API = "https://filters-zeta.vercel.app/api/filter"

if "ai_history" not in st.session_state:
    st.session_state.ai_history = []

if "math_history" not in st.session_state:
    st.session_state.math_history = [] 

def check_prompt(prompt):
    try:
        response = requests.post(
            FILTER_API,
            json={"prompt":prompt},
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return(
            data.get("ok", False),
            data.get("reason", "")
        )

    except Exception as e:
        return False, str(e)

def generate(prompt):
  system_prompt = """
  You are a helpful AI teaching Assistant.
  explain concepts clearly and simply.
  use examples when useful.
  structure your answers with headings or bullet points when apropriate.
  adapt the explanation to the user's question and level
  """
  try:
    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[
         {"role": "user", "content": system_prompt},
         {
            "role": "user",
            "content": prompt
         }
        ],
        temperature=0.3,
        max_tokens=512
    )

    return response.choices[0].message.content

  except Exception as e:
    return "Error: "+ str(e)

SYSTEM_PROMPT="""
you are a math mastermind
solve the problem step by step
Explain the reasoning clearly.
give the final answer.
verify the answer if possible.
adapt the explanation to the requested difficulty level.
"""
def solve_math(problem,level):
  prompt=f"""
  {SYSTEM_PROMPT}
  level:{level}
  Problem:{problem}
  """
  try:
    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[
         {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=1024
    )

    return response.choices[0].message.content
  except Exception as e:
     return f"Error: {e}"

st.sidebar.title("🤖 AI Mastermind Hub")

option = st.sidebar.radio(
   "choose an application:",
   [
      "🤖 AI teaching Assistant",
      "🧮 Math Mastermind",
      "🖼️ AI Image Generator"
   ]
)

st.title("🤖  AIMastermind Hub")

st.write(
   "choose a tool from sidebar to start learning" 
   "solving problems, or crearing images."
)

if option == "🤖 AI Teaching Assistant":

   st.header("🤖 AI Teaching Assistant")
   st.write(
      "Ask questions about different subjects "
      "and get an AI generated explenation."
   )

   question = st.text_input(
      "Enter your question here:",
      placeholder="Example: Explain photosynthesis simply."
   )

   if st.button("Ask", type="Primary"):
      if question.strip():
         with.st.spinner("Generating response..."):
           answer = generate(question)
