# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import google.generativeai as genai
# import os
# from dotenv import dotenv_values, load_dotenv

# app = FastAPI()
# load_dotenv()

# API_KEY = os.getenv("API_KEY")


# class Query(BaseModel):
#     message: str
#     api_key: str = ""

# from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # You can specify the exact domains you want to allow
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all methods like GET, POST, OPTIONS, etc.
#     allow_headers=["*"],  # Allow all headers
# )


# @app.post("/ask")
# async def ask_ai(query: Query):
#     global API_KEY
#     key = query.api_key if query.api_key else API_KEY
#     if not key:
#         raise HTTPException(status_code=400, detail="Api Key is Required.")

#     try:
#         genai.configure(api_key=key)
#         model = genai.GenerativeModel("gemini-pro")
#         response = model.generate_content(query.message)
#         return {"reply": response.text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()
# load_dotenv()

# API_KEY = os.getenv("API_KEY")

# # Middleware for CORS to allow frontend interaction
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Store chat history
# chat_history = []

# class Query(BaseModel):
#     message: str
#     api_key: str = ""

# @app.post("/ask")
# async def ask_ai(query: Query):
#     global API_KEY
#     key = query.api_key if query.api_key else API_KEY
#     if not key:
#         raise HTTPException(status_code=400, detail="API Key is Required.")

#     try:
#         genai.configure(api_key=key)
#         model = genai.GenerativeModel("gemini-pro")
#         response = model.generate_content(query.message)

#         # Add query and response to chat history
#         chat_history.append({"role": "user", "message": query.message})
#         chat_history.append({"role": "ai", "message": response.text})

#         return {"reply": response.text, "chat_history": chat_history}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
load_dotenv()

API_KEY = os.getenv("API_KEY")

# Middleware for CORS to allow frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store chat history
chat_history = []

# Initial welcome message to introduce the Python tutor
WELCOME_MESSAGE = "Hello! I'm your Python Tutor. I'm here to help you learn Python programming step-by-step. Ask me anything about Python, and I'll guide you through it."

class Query(BaseModel):
    message: str
    api_key: str = ""

@app.post("/ask")
async def ask_ai(query: Query):
    global API_KEY
    key = query.api_key if query.api_key else API_KEY
    if not key:
        raise HTTPException(status_code=400, detail="API Key is Required.")

    # Adding the welcome message to the chat history if it's the first message
    if not chat_history:
        chat_history.append({"role": "ai", "message": WELCOME_MESSAGE})

    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-pro")
        
        # Construct a custom prompt with Python tutor context
        tutor_prompt = f"""
        You are a Python Tutor. Your student asks: "{query.message}"

        Please explain this concept in a simple and clear way, suitable for a beginner. Break it down into easy-to-understand steps and provide multiple examples wherever applicable. Include the following:
        1. A basic explanation of the concept.
        2. Real-life analogies to help the student understand better.
        3. One or more examples of how the concept is used in Python code, with an explanation of each step in the example.
        4. Any common mistakes beginners might make, and how to avoid them.
        5. If applicable, suggest resources or next steps the student can take to learn more about this topic.

        Your goal is to make the concept as approachable and understandable as possible for a new Python learner. Be friendly and patient in your response!
        """
        response = model.generate_content(tutor_prompt)

        # Add query and response to chat history
        chat_history.append({"role": "user", "message": query.message})
        chat_history.append({"role": "ai", "message": response.text})

        return {"reply": response.text, "chat_history": chat_history}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
