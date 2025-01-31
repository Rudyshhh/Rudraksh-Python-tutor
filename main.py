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

class Query(BaseModel):
    message: str
    api_key: str = ""

@app.post("/ask")
async def ask_ai(query: Query):
    global API_KEY
    key = query.api_key if query.api_key else API_KEY
    if not key:
        raise HTTPException(status_code=400, detail="API Key is Required.")

    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(query.message)

        # Add query and response to chat history
        chat_history.append({"role": "user", "message": query.message})
        chat_history.append({"role": "ai", "message": response.text})

        return {"reply": response.text, "chat_history": chat_history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
