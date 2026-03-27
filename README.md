# 🚗 Car Agentic Chatbot

## 1. Introduction

Car Agentic Chatbot is an intelligent AI system built with an **Agentic AI architecture** to assist users in automotive-related tasks such as:

* Car recommendations
* Basic fault diagnosis
* Maintenance suggestions
* Technical document retrieval

Unlike traditional chatbots, this system can **plan actions, call tools, and perform multi-step reasoning** to generate more accurate and context-aware responses.

---

## 3. Core Components

### 3.1 Agent (Core Brain)

* Powered by LLMs (Gemini / GPT / LLaMA)
* Capabilities:

  * Intent understanding
  * Multi-step planning
  * Tool selection and orchestration

### 3.2 Tool System

The agent interacts with external tools to extend its capabilities:

| Tool                | Function                     |
| ------------------- | ---------------------------- |
| Car Diagnostic Tool | Analyze vehicle issues       |
| Weather API         | Retrieve weather data        |
| Map API             | Suggest routes               |
| IoT Sensor          | Receive camera / sensor data |

---

### 3.3 RAG (Retrieval-Augmented Generation)

* Uses a Vector Database to store:

  * Car manuals
  * Repair guides
  * FAQs

**Flow:**

1. User query
2. Convert to embedding
3. Retrieve relevant documents
4. Inject into prompt
5. Generate final answer

---

## 4. Agentic Workflow

```
<p align="center">
  <img src="./assets/Workflow.png" width="700"/>
</p>
---

## 5. Example Use Case

### Input:

"My car makes a strange noise when braking"

### Agent Behavior:

1. Detect intent: mechanical issue
2. Plan actions:

   * Retrieve knowledge from database
   * Call diagnostic tool
3. Combine results
4. Return:

   * Possible causes
   * Risk level
   * Repair recommendations

---

## 6. Technologies Used

### 🔹 AI / ML

* LLMs: Gemini / GPT
* Embedding models
* Transformers

### 🔹 Backend

* Python
* FastAPI
* LangChain / Agent frameworks

### 🔹 Data

* Vector Database (FAISS / Chroma)

### 🔹 IoT Integration

* MQTT
* Camera (YOLO-based detection)

---

## 7. Installation & Setup

### 7.1 Clone Repository

```bash
git clone <repo>
cd car-agentic-chatbot
```

### 7.2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 7.3 Environment Configuration (.env)

```env
API_KEY=your_api_key
MQTT_BROKER=your_broker
```

### 7.4 Run the System

```bash
uvicorn main:app --reload
```

---

## 8. Demo

### Use cases:

* Web chat interface
* IoT camera streaming
* Real-time AI detection and response

---

## 9. Evaluation

Evaluation is based on real-world demo scenarios:

* Response accuracy
* Multi-step reasoning capability
* Latency
* IoT integration performance

---

## 10. Future Work

* Multi-agent collaboration
* Voice assistant integration
* Predictive maintenance
* Domain-specific fine-tuning for automotive

---

## 11. Self-Learning Outcomes

During this project, the following skills were self-developed:

* Agentic AI architecture design
* RAG pipeline implementation
* AI + IoT integration

---

## 12. Conclusion

Car Agentic Chatbot represents a shift from traditional chatbots to **intelligent systems capable of reasoning and acting**, making it highly applicable to real-world automotive use cases.
