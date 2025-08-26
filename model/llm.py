from langchain_groq import ChatGroq


API_KEY = ""

def model():
    return ChatGroq(model="gemma2-9b-it", api_key=API_KEY)

# print(model().invoke("HI"))