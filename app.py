import streamlit as st
import google.generativeai as genai
import requests
import base64

# -- Page Configuration --
st.set_page_config(page_title="Codebase Analyzer Pro", page_icon="🧠", layout="wide")

# -- Security & API Key --
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("System configuration error: API Key not found in vault.")
    st.stop()

genai.configure(api_key=api_key)
# Utilizing the latest model architecture
model = genai.GenerativeModel('gemini-3.5-flash')

# -- UI Header --
st.title("🧠 Advanced GitHub Architecture Analyzer")
st.markdown("Dynamic codebase evaluation, language analytics, and AI-powered context exploration.")
st.divider()

# -- Advanced GitHub Scraper Engine --
@st.cache_data(show_spinner=False)
def fetch_advanced_github_context(repo_path):
    headers = {"Accept": "application/vnd.github.v3+json"}
    repo_data = {}
    context_string = f"Target Repository: {repo_path}\n\n"
    
    # 1. Fetch Core Metadata
    repo_res = requests.get(f"https://api.github.com/repos/{repo_path}", headers=headers)
    if repo_res.status_code == 200:
        data = repo_res.json()
        repo_data['description'] = data.get('description', 'No description provided.')
        repo_data['stars'] = data.get('stargazers_count', 0)
        repo_data['forks'] = data.get('forks_count', 0)
        context_string += f"Description: {repo_data['description']}\n\n"
    else:
        return None, None

    # 2. Fetch Language Analytics
    lang_res = requests.get(f"https://api.github.com/repos/{repo_path}/languages", headers=headers)
    if lang_res.status_code == 200:
        repo_data['languages'] = lang_res.json()
        context_string += f"Tech Stack / Languages: {list(repo_data['languages'].keys())}\n\n"

    # 3. Fetch README Context
    readme_res = requests.get(f"https://api.github.com/repos/{repo_path}/readme", headers=headers)
    if readme_res.status_code == 200:
        readme_data = readme_res.json()
        readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
        context_string += f"--- CORE DOCUMENTATION (README.md) ---\n{readme_content}\n\n"
        
    # 4. Fetch File Tree (Root Level)
    contents_res = requests.get(f"https://api.github.com/repos/{repo_path}/contents", headers=headers)
    if contents_res.status_code == 200:
        files = [item['name'] for item in contents_res.json() if item['type'] == 'file']
        dirs = [item['name'] for item in contents_res.json() if item['type'] == 'dir']
        context_string += f"--- DIRECTORY STRUCTURE ---\nFiles: {', '.join(files)}\nDirectories: {', '.join(dirs)}\n"
        
    return context_string, repo_data

# -- Main Application Logic --
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Repository Target")
    repo_input = st.text_input("Enter Repository (owner/repo)", placeholder="e.g., scikit-learn/scikit-learn")
    
if repo_input:
    with st.spinner("Executing API calls and scraping repository architecture..."):
        repo_context, repo_metrics = fetch_advanced_github_context(repo_input)
        
    if not repo_context:
        st.error("Repository not found or API rate limit exceeded. Check the format (owner/repo).")
    else:
        # Create Tabs for a professional UI
        tab1, tab2 = st.tabs(["💬 AI Chat Interface", "📊 Repository Analytics"])
        
        with tab2:
            st.subheader("Metrics & Architecture")
            st.write(f"**Description:** {repo_metrics.get('description')}")
            col_a, col_b = st.columns(2)
            col_a.metric("Stars", repo_metrics.get('stars', 0))
            col_b.metric("Forks", repo_metrics.get('forks', 0))
            
            st.write("**Language Breakdown:**")
            if repo_metrics.get('languages'):
                for lang, bytes_count in repo_metrics['languages'].items():
                    st.progress(min(bytes_count / sum(repo_metrics['languages'].values()), 1.0), text=lang)
        
        with tab1:
            if "messages" not in st.session_state:
                st.session_state.messages = []
                
                # Highly specialized system prompt
                st.session_state.context_prompt = (
                    "You are a Senior AI & Machine Learning Engineer conducting a code review. "
                    f"Analyze the following repository context:\n{repo_context}\n"
                    "Provide highly technical, accurate, and structured answers. Evaluate algorithmic complexity "
                    "and best practices where applicable."
                )

            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            if prompt := st.chat_input("Query the codebase architecture..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    try:
                        full_prompt = f"{st.session_state.context_prompt}\n\nUser Query: {prompt}"
                        response = model.generate_content(full_prompt)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"Error communicating with AI engine: {e}")