# 🚗 Car Agentic Chatbot

## 1. Introduction

Car Agentic Chatbot is an intelligent AI system built with an **Agentic AI architecture** to assist users in automotive-related tasks such as:

* Car recommendations
* Maintenance suggestions
* Polichy document retrieval
* Car information retrieval
* Filt cars by user's demand (price, seats, fuel type,...)
* Compare cars's differences

Unlike traditional chatbots, this system can **plan actions, call tools, and perform multi-step reasoning** to generate more accurate and context-aware responses.

---

## 2. Core Components

### 2.1 Agent (Core Brain)

* Powered by LLMs (Qwen3)
* Capabilities:

  * Intent understanding
  * Generate response with knowledge

### 2.2 Tool System (Not yet)

The agent interacts with external tools to extend its capabilities:

| Tool                | Function                     |
| ------------------- | ---------------------------- |
| Car Diagnostic Tool | Analyze vehicle issues       |
| Weather API         | Retrieve weather data        |
| Map API             | Suggest routes               |
| IoT Sensor          | Receive camera / sensor data |

---

### 2.3 RAG (Retrieval-Augmented Generation)

* Uses a Vector Database to store:

  * Cars's information
  * Policy documentary
---

## 3. Agentic Workflow

<p align="center">
  <img src="./assert/Workflow.png" width="700"/>
</p>

**Workflow Explanation:**

1. The user submits a query
2. The agent detects the intent
3. The system plans required actions
4. It may call tools, APIs, or retrieve knowledge (RAG)
5. Results are aggregated
6. A final response is generated

---

## 4. Example Use Case

### Input:

"Tôi cần 1 chiếc xe 5 chỗ ngồi, động cơ xăng, tầm giá dưới 1 tỷ."

### Agent Behavior:

1. Detect intent: Ask recommendation
2. Plan actions:

   * List all customer's demands about the car
   * Retrieve most suitable cars from database
3. Combine results
4. Return:

   * List all the suitable cars
   * List cars's demanded information

---

## 5. Technologies Used

### 🔹 AI / ML

* LLMs: Gemini / GPT
* Embedding models
* Transformers

### 🔹 Backend

* Python
* FastAPI (Not yet)
* LangChain / Agent frameworks

### 🔹 Data

* Vector Database (FAISS / Chroma)
---

## 6. Installation & Setup

### 6.1 Clone Repository

```bash
git clone https://github.com/trandoducphat/Car-Agentic-Chatbot.git
cd Car-Agentic-Chatbot
```

### 6.2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 6.3 Run the model

```bash
python main.py
```
---

## 7. Evaluation

Evaluation is based on real-world demo scenarios:

* Response accuracy, naturally
* Multi-step reasoning capability
* Latency

---

## 8. Future Work

* Agent can predict manuals
* UI + Database system 
* Domain-specific fine-tuning for automotive

---

## 9. Self-Learning Outcomes

During this project, the following skills were self-developed:

* Agentic AI architecture design
* RAG pipeline implementation
* AI + IoT integration

---

## 10. Conclusion

Car Agentic Chatbot represents a shift from traditional chatbots to **intelligent systems capable of reasoning and acting**, making it highly applicable to real-world automotive use cases.