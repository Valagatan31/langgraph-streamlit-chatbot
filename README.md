# LangGraph Streamlit Chatbot

This project is a multi-threaded AI chatbot built using **LangGraph**, **Streamlit**, and **Google Gemini (Generative AI)**.  
It supports conversation memory using **SQLite checkpointing**, allowing users to switch between multiple chat threads.


## Features
- Multi-conversation (thread-based) chat support
- Persistent chat memory using SQLite
- Streaming AI responses
- Built with LangGraph state management
- Simple and clean Streamlit UI

##  Tech Stack
- Python
- Streamlit
- LangGraph
- LangChain
- Google Gemini (Generative AI)
- SQLit

---

##  Setup Instructions

###  Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/langgraph-streamlit-chatbot.git
cd langgraph-streamlit-chatbot


pip install -r requirements.txt

streamlit run frontend.py

