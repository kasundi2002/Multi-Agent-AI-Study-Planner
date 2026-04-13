# 🧠 Multi-Agent AI Study Planner

## 📌 Project Overview

This project implements a **Multi-Agent AI Study Planner System** that automatically generates a structured learning plan for a given subject.

The system uses **multiple AI agents** that collaborate to:

- Break down a subject into learning topics
- Organize topics logically
- Find learning resources
- Generate a study schedule

This project is developed for **SE4010 – CTSE Assignment 2**.

---

## 🧠 Multi-Agent Architecture

The system consists of 4 agents:

### 🧠 Planner Agent
- Breaks subject into learning topics

### 🧩 Content Structurer Agent
- Organizes topics from beginner to advanced

### 🔎 Resource Finder Agent
- Finds learning resources

### 📅 Scheduler Agent
- Creates study schedule

---

## 🔁 Workflow

User Input
↓
Planner Agent
↓
Structurer Agent
↓
Resource Finder Agent
↓
Scheduler Agent
↓
Final Study Plan


---

## 🛠 Tools Used

Each agent uses custom Python tools:

- `load_topics()`
- `organize_topics()`
- `find_resources()`
- `create_schedule()`
- `save_plan()`

---

## 🧠 Global State Management

The system uses a shared global state:

```python
state = {
    "goal": "",
    "topics": [],
    "structured_topics": [],
    "resources": {},
    "schedule": ""
}
```

## ⚙️ Tech Stack
Python
CrewAI
Ollama (Local LLM)
Llama3 / Phi3
LangChain

## 📁 Project Structure

        AI-Study-Planner/
        │
        ├── agents/
        │   ├── planner_agent.py
        │   ├── structurer_agent.py
        │   ├── resource_agent.py
        │   └── scheduler_agent.py
        │
        ├── tools/
        │   ├── planner_tool.py
        │   ├── structurer_tool.py
        │   ├── resource_tool.py
        │   └── scheduler_tool.py
        │
        ├── tests/
        │
        ├── main.py
        ├── state.py
        ├── requirements.txt
        └── README.md

## 🚀 Installation
1. Clone Repository
git clone <repo-url>
cd AI-Study-Planner
2. Create Virtual Environment
python -m venv venv
Activate:
Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Install Ollama

Download from:
https://ollama.com

Pull model:
ollama pull llama3
▶️ Run Project
python main.py
🧪 Testing

Run tests:
pytest

## 👥 Team Members
Name	Agent	Tool
Member 1	Planner Agent	load_topics
Member 2	Structurer Agent	organize_topics
Member 3	Resource Agent	find_resources
Member 4	Scheduler Agent	create_schedule

## 📄 Assignment

SE4010 – CTSE
Assignment 2 – Multi-Agent System
