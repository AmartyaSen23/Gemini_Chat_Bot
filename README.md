# 🤖 GitHub Codebase & Architecture Analyzer

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg?logo=python&logoColor=white)](https://www.python.org)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://geminichatbo-2xtnvtu7sjhsrgjdszw34n.streamlit.app/)

## Overview
This project is an advanced, AI-driven GitHub Repository Analyzer built with Python, Streamlit, and the Gemini API. It transcends basic chatbots by dynamically scraping repository architecture, file structures, and documentation via the GitHub REST API, injecting this context directly into the Gemini Engine for deep codebase analysis.

Designed with a focus on algorithmic complexity and data science best practices, this tool acts as a virtual Senior Engineer, capable of explaining complex logic, identifying dependencies, and suggesting optimizations.

## 🚀 Key Features
* **Dynamic Context Injection:** Automatically fetches and processes `README.md`, root file structures, and repository metadata.
* **Repository Analytics:** Retrieves and visualizes the primary programming languages utilized in the target repository.
* **Context-Aware AI Chat:** Leverages `gemini-2.5-flash` to answer highly specific questions about the codebase.
* **Secure Architecture:** Built with environment-level secret management to protect API credentials.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Frontend/Framework:** Streamlit
* **AI Engine:** Google Generative AI (Gemini 2.5 SDK)
* **API Integration:** GitHub REST API (`requests`)

## ⚙️ Installation & Deployment
### 1. Clone the repository.
### 2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

   ```

### 3. Set your `GEMINI_API_KEY` in your environment variables or Streamlit secrets vault.
### 4. Run the application:
   ```bash
   streamlit run app.py
   ```



**Author:** Amartya Sen

```
