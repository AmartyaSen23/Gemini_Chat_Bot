import streamlit as st
import google.generativeai as genai
import requests
import base64

st.set_page_config(page_title="GitHub Repo Analyzer", page_icon="🤖")

# Changed to sound highly professional
st.title("🤖 GitHub Repository Analyzer")
st.markdown("Analyze and chat with the architecture and codebase of any public GitHub repository.")

# Securely pull the API key from Streamlit's encrypted secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("System configuration error: API Key not found.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

repo_input = st.text_input("Target GitHub Repository (Format: owner/repo)")

@st.cache_data(show_spinner=False)
def fetch_github_context(repo_path):
    headers = {"Accept": "application/vnd.github.v3+json"}
    context = f"Repository: {repo_path}\n\n"
    
    repo_res = requests.get(f"https://api.github.com/repos/{repo_path}", headers=headers)
    if repo_res.status_code == 200:
        data = repo_res.json()
        context += f"Description: {data.get('description', 'No description')}\n"
        context += f"Language: {data.get('language', 'Unknown')}\n\n"
    
    readme_res = requests.get(f"https://api.github.com/repos/{repo_path}/readme", headers=headers)
    if readme_res.status_code == 200:
        readme_data = readme_res.json()
        readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
        context += f"--- README.md ---\n{readme_content}\n\n"
        
    contents_res = requests.get(f"https://api.github.com/repos/{repo_path}/contents", headers=headers)
    if contents_res.status_code == 200:
        files = [item['name'] for item in contents_res.json() if item['type'] == 'file']
        dirs = [item['name'] for item in contents_res.json() if item['type'] == 'dir']
        context += f"--- Root Files ---\n{', '.join(files)}\n"
        context += f"--- Root Directories ---\n{', '.join(dirs)}\n"
        
    return context

if repo_input:
    with st.spinner(f"Analyzing {repo_input}..."):
        repo_context = fetch_github_context(repo_input)
        
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.context_prompt = f"You are a helpful AI assistant analyzing a GitHub repository. Here is the repository context:\n{repo_context}\nAnswer user questions based on this."

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a question about the codebase..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                full_prompt = f"{st.session_state.context_prompt}\n\nUser Question: {prompt}"
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error communicating with AI engine: {e}")