# ⚖️ AI Chained Comparator

A full-stack AI application built with **Streamlit** and the **Google Gemini 2.5 Flash** model that demonstrates the power of **LLM Chaining**.

Instead of a single, complex AI prompt, this application breaks down the problem into three distinct, structured Large Language Model (LLM) calls:
1. **Call 1:** Independently analyzes Item A.
2. **Call 2:** Independently analyzes Item B.
3. **Call 3:** Ingests the previous analyses and renders a final verdict.

By chaining LLMs in this way, the application prevents hallucinations, ensures objective analysis, and produces a highly structured and reliable comparison between any two concepts, technologies, or ideas.

## 🚀 Features
- **LLM Chaining Architecture:** Demonstrates multi-step prompt engineering.
- **Google GenAI SDK:** Uses the latest `google-genai` library and the `gemini-2.5-flash` model.
- **Custom Prompts:** Clean separation of concerns with system instructions abstracted into a separate `prompts.py` file.
- **Clean UI:** A completely custom, professional interface built with Streamlit (with default Streamlit branding hidden).

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <your-github-repo-url>
   cd AiComparator
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API Key**
   Create a `.env` file in the root directory and add your Google Gemini API Key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

5. **Run the Application**
   ```bash
   python -m streamlit run app.py
   ```

## 🧠 How it Works Under the Hood
1. The user inputs two items (e.g., "React.js" and "Vue.js").
2. The app triggers two independent asynchronous calls to Gemini with a strict system prompt (`ANALYZE_PROMPT`).
3. Once both analyses are returned, the app combines them into a unified context and triggers a final call with a different system prompt (`COMPARE_PROMPT`).
4. The frontend renders the intermediate steps and the final verdict dynamically.

---
*Built as a first exploration into Prompt Engineering and LLM orchestration.*
