Chat Bot With Persona 🤖🇮🇳

A full‑stack demo that pairs Groq’s Llama‑3 LLM with LangGraph 
(checkpointed in MongoDB) and exposes two entry‑points:

Interface	File	Purpose
CLI	main.py	Terminal chat loop (persistent)
Web	streamlit_app.py	Two‑page Streamlit UI

The bot speaks in a Hinglish (Hindi + English) casual tone by default, and
all chat history is resume‑able via a session ID.

⸻

🌟 Features
	•	Groq API – low‑latency streaming from Llama‑3‑70B‑8192
	•	LangGraph state machine with a single llm_node
	•	MongoDBSaver checkpointing → resume any conversation by ID
	•	Streamlit 1.32+ UI

⸻

🗂 Project structure

├── checkpointer.py      # Returns MongoDBSaver
├── groq_client.py       # Thin Groq wrapper (loads Groq API‑key)
├── langgraph_flow.py    # StateGraph creation
├── main.py              # CLI chat loop
├── streamlit_app.py     # Web front‑end
├── requirements.txt
└── README.md

⸻

🚀 Quick start (local)

# 1. Clone and enter the repo
git clone https://github.com/mishalalex/chatbot-with-persona.git
cd chatbot-with-persona

# 2. Python venv + deps
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt  # to install all the requirements

# 3. MongoDB (local or Atlas)
# Local quick‑start (docker):
docker compose up -d mongodb        # provided in the docker‑compose.yaml file

# 4. .env
cp .env.example .env  # then edit with your keys

# 5a. CLI interface
python main.py

# 5b. Streamlit UI
streamlit run streamlit_app.py

⸻

🖥️ Usage tips
	•	New session → leave the ID blank, one is auto‑generated.
	•	Resume → paste a previous ID on Page 1.
	•	All messages (user + assistant) are stored minus the system prompt.
	•	LangGraph injects the Hinglish system prompt on every call.
