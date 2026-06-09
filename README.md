<div align="center">

# 🎓 University Admission AI Assistant

### *Your Intelligent Campus Guide — Powered by IBM Granite & RAG*

[![IBM watsonx.ai](https://img.shields.io/badge/IBM-watsonx.ai-0530AD?style=for-the-badge&logo=ibm&logoColor=white)](https://www.ibm.com/watsonx)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F00?style=for-the-badge)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<br/>

> **Never let a student leave with the wrong answer.**  
> This AI-powered admission agent retrieves verified university policies in real time,  
> answers student queries with factual accuracy, and refuses to hallucinate — guaranteed.

<br/>

![Demo Banner](https://placehold.co/900x300/0530AD/FFFFFF?text=🎓+University+Admission+AI+Assistant&font=montserrat)

</div>

---

## 📌 Table of Contents

- [✨ Features](#-features)
- [🧠 How It Works (RAG Architecture)](#-how-it-works-rag-architecture)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Configuration](#️-configuration)
- [📁 Project Structure](#-project-structure)
- [💬 What You Can Ask](#-what-you-can-ask)
- [🛡️ Guardrails & Safety](#️-guardrails--safety)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **IBM Granite LLM** | Powered by `ibm/granite-8b-code-instruct` via watsonx.ai |
| 📚 **RAG Pipeline** | Retrieves verified university policy chunks before every answer |
| 🔒 **Hallucination Guard** | Refuses to answer if data isn't found in the knowledge base |
| 🗂️ **Vector Search** | ChromaDB + SentenceTransformers for semantic document retrieval |
| 💬 **Chat Memory** | Full conversational context retained across the session |
| 🎨 **Clean Streamlit UI** | Zero-friction interface — no technical knowledge needed |
| 🌐 **Multilingual Ready** | Supports queries in Hindi & English |

---

## 🧠 How It Works (RAG Architecture)

```
┌─────────────────────────────────────────────────────────────────┐
│                        STUDENT QUERY                            │
│            "What is the fee for B.Tech CSE?"                    │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              ChromaDB Vector Store (Local)                       │
│     university_data.txt  →  Chunked  →  Embedded  →  Stored    │
│                                                                  │
│  Query → Semantic Search → Top 3 Relevant Policy Chunks         │
└───────────────────────────┬─────────────────────────────────────┘
                            │  Retrieved Context
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Prompt Engineering                            │
│   System Role + Strict Rules + Context Docs + Student Question  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│             IBM Granite 8B (via watsonx.ai)                      │
│          Greedy Decoding · Temperature 0.0 · 400 Tokens         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
                  ✅ Factual, Grounded Answer
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/university-admission-agent.git
cd university-admission-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> **requirements.txt** should include:
> ```
> streamlit
> ibm-watsonx-ai
> chromadb
> sentence-transformers
> ```

### 3. Add Your University Data

Create a `university_data.txt` file in the project root and populate it with your university's official policies, fee structures, deadlines, and eligibility criteria — separated by blank lines.

```
[DOCUMENT: Deadlines]
Fall 2026 application deadline is August 15, 2026.
Late applications will be accepted until September 1 with a penalty fee of ₹500.

[DOCUMENT: Fees - B.Tech CSE]
The tuition fee for B.Tech Computer Science is ₹85,000 per semester.
The one-time non-refundable registration fee is ₹10,000.
```

### 4. Launch the App

```bash
streamlit run app.py
```

### 5. Enter IBM Cloud Credentials

Open the sidebar and provide:
- 🔑 **IBM Cloud API Key**
- 🗂️ **watsonx.ai Project ID**

> **Get these from:** [IBM Cloud Console](https://cloud.ibm.com) → watsonx.ai → Project Settings

---

## ⚙️ Configuration

All key parameters are set directly in `app.py`. Here's a quick reference:

| Parameter | Value | Purpose |
|---|---|---|
| `model_id` | `ibm/granite-8b-code-instruct` | The IBM Granite LLM |
| `decoding_method` | `greedy` | Ensures deterministic, factual output |
| `temperature` | `0.0` | Zero creativity — maximizes accuracy |
| `max_new_tokens` | `400` | Controls response length |
| `n_results` | `3` | Number of policy chunks retrieved per query |
| `embedding_model` | `all-MiniLM-L6-v2` | Local sentence embeddings (free, fast) |

---

## 📁 Project Structure

```
university-admission-agent/
│
├── app.py                  # Main Streamlit application
├── university_data.txt     # 📄 Your university's knowledge base (add your data here!)
├── requirements.txt        # Python dependencies
├── README.md               # You are here!
└── .env (optional)         # IBM_API_KEY, IBM_PROJECT_ID (for local development)
```

> 💡 **Tip:** Use a `.env` file with `python-dotenv` to avoid entering credentials on every launch.

---

## 💬 What You Can Ask

The assistant is trained to answer questions across these categories:

<details>
<summary><b>📅 Deadlines & Timelines</b></summary>

- What is the last date to submit the online application for 2026?
- When will the first merit cutoff list be announced?
- What is the deadline to withdraw admission and claim a refund?
</details>

<details>
<summary><b>⚙️ Eligibility & Lateral Entry</b></summary>

- What is the minimum percentage required for B.Tech CSE?
- Can a commerce student apply for the BCA program?
- What is the eligibility for direct lateral entry into B.Tech second year?
</details>

<details>
<summary><b>💰 Fees & Hostel Charges</b></summary>

- What is the tuition fee per semester for B.Tech CSE?
- What are the annual hostel charges and does it include food?
- What is the fine rate per day for late fee payment?
</details>

<details>
<summary><b>🎓 Scholarships & Financial Aid</b></summary>

- What are the criteria for a 100% tuition fee waiver?
- What minimum CGPA is needed to renew the scholarship?
- Is there a sibling discount on tuition fees?
</details>

<details>
<summary><b>🏢 Placements & Campus Life</b></summary>

- What is the average placement package for CSE graduates?
- Which top recruiters visit the campus?
- Can I change my branch after the first year?
</details>

---

## 🛡️ Guardrails & Safety

This assistant is built with **strict factual grounding**:

```
❌  "Does the campus have a swimming pool?"
✅  Bot Response: "I am sorry, I cannot find that information in our official
    guidelines. Please contact our central admissions office directly at
    admissions@university.edu."
```

The model is **explicitly instructed to never invent facts**. If the answer isn't in `university_data.txt`, it will say so — every single time.

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: your feature description"`
4. Push and open a Pull Request

Please ensure any new features respect the **no-hallucination guardrail** principle.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ using **IBM watsonx.ai** · **Granite 8B** · **Streamlit** · **ChromaDB**

⭐ *Star this repo if it helped you build something awesome!* ⭐

</div>
