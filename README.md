# THE-AI-AGENT-FACTORY: Aina Digital FTE

The AI Agent Factory is a robust framework for deploying autonomous Digital Full-Time Employees (FTEs). **Aina** is its premier agent, engineered to monitor diverse communication channels (WhatsApp, Gmail), extract high-precision tasks using LLMs, and maintain a professional persona.

## 🏗️ Architecture: How Aina Works

Aina operates on a modular architecture designed for security, portability, and professional agency.

### 1. 📜 Constitution & Governance
Governed by a core **Constitution** (`CONSTITUTION.md`), Aina adheres to non-negotiable principles:
- **Digital FTE First**: High autonomy and goal-alignment.
- **Strict Session Security**: Secure, encrypted handling of all session states.
- **Professional Agency**: Courteous, goal-oriented interactions.

### 2. 🆔 Identity Framework
The **Identity** (`IDENTITY.md`) module defines the agent's persona. It ensures that Aina acts as a distinct, professional entity, reducing human overhead while maintaining organizational standards.

### 3. 📡 Gateway & Monitoring
Aina integrates with the **OpenClaw Gateway** to monitor real-time communication. It supports multi-channel filtering, ensuring only authorized group chats or threads are processed.

### 4. 🧠 Intelligence & Extraction
Utilizing **Google Gemini LLM**, Aina transforms unstructured messages into structured tasks. It normalizes deadlines, identifies assignees, and calculates confidence scores for every extraction.

### 5. 📧 Gmail Skill
Beyond instant messaging, Aina can scan and filter Gmail inboxes for specific recruitment or project-related keywords, bridging the gap between chat and email.

---

## 🚀 Quick Setup

Aina is designed for rapid, secure deployment. Follow these steps to get started:

### 1. Prerequisites
- Python 3.12+
- Access to [OpenClaw Gateway](https://github.com/openclaw/gateway)

### 2. Environment Configuration
We use environment variables for all sensitive configurations. Copy the template and fill in your details:
```bash
cp .env.example .env
```
Edit `.env` with your API keys:
- `OPENCLAW_API_KEY`: Your OpenClaw authentication token.
- `GEMINI_API_KEY`: Your Google Gemini API key.
- `GATEWAY_URL`: The WebSocket URI for your OpenClaw instance.

### 3. Installation
Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 4. Running the Agent
Start the Aina engine:
```bash
python main.py
```

---

## 🛠️ Development & Portability
- **Zero Hardcoding**: No local paths or PII are hardcoded.
- **SDD Discipline**: All features are built using Spec-Driven Development.
- **Data Safety**: Sensitive data is never logged in plaintext.

*Built with ❤️ for the AI Agent Factory.*
