🧠 MindCare AI

An AI-powered multi-agent mental wellness assistant built using Python, Streamlit, and Groq API.

MindCare AI helps users reflect on their emotional wellbeing through specialised AI agents that provide emotional assessment, practical coping strategies, long-term wellness guidance, and crisis-aware support resources in a simple and interactive interface.

🔗 Live Demo: https://mindcare-ai-assistant.streamlit.app/

✨ Features
🤖 Multi-agent AI workflow
🧠 Emotional wellness assessment
🎯 Personalised coping strategies
🔄 Long-term wellness planning
🚨 Crisis keyword detection system
📈 Mood and stress tracking
🎨 Modern animated Streamlit UI
🔒 Privacy-conscious session tracking
🏗️ System Architecture
User Input
   ↓
Orchestrator
   ├── Assessment Agent
   ├── Action Agent
   └── Follow-up Agent
   ↓
Combined Wellness Response

The orchestrator coordinates all specialised AI agents and manages safety routing through the crisis detection system.

🧩 Tech Stack
Python
Streamlit
Groq API
Llama Models
Custom CSS
JSON-based session tracking

📸 Screenshots

🏠 Landing Page

📝 Wellness Assessment Form

📊 AI Wellness Report

🔐 Privacy
MindCare AI follows a privacy-conscious design approach.
The application:
does not permanently store personal emotional descriptions
does not require signup or authentication
only temporarily stores anonymous wellness metrics for progress tracking

Stored metrics include:
emotional state score
stress level
sleep duration
timestamp

This allows users to visualise progress while minimising personal data storage.

⚙️ Local Setup
1. Clone the Repository
git clone https://github.com/VajraKalekar/mental-wellbeing-agent.git
cd mental-wellbeing-agent

3. Install Dependencies
pip install -r requirements.txt

4. Add Environment Variables
Create a .env file and add:
GROQ_API_KEY=your_api_key_here

5. Run the Application
streamlit run app.py

📂 Project Structure
mental-wellbeing-agent/
│
├── agents/
│   ├── assessment_agent.py
│   ├── action_agent.py
│   └── followup_agent.py
│
├── utils/
│   └── groq_client.py
│
├── app.py
├── orchestrator.py
├── tracker.py
├── charts.py
├── requirements.txt
└── session_data.json

⚠️ Disclaimer
This project is designed for emotional wellness support and educational purposes only.

It is not a replacement for professional mental health care, diagnosis, therapy, or emergency services.

If someone is in immediate crisis or danger, they should contact a professional helpline or emergency support service immediately.

🚀 Future Improvements
Secure cloud database integration
User authentication
Multilingual support
Voice interaction
Mobile-first experience
Advanced analytics dashboard
Journaling and reflection tools

👨‍💻 Author
Vajra Kalekar
Final Year Major Project — AI-Powered Mental Wellness Support System
