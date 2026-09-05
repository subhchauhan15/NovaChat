import streamlit as st
import time
from retrival import main

# ── Page config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="NovaChat – AI Policy Assistant",
    page_icon="🚀",
    layout="centered",
)

# ── Custom CSS for a premium dark-terminal aesthetic ─────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─── Global ─── */
:root {
    --bg-primary: #0d1117;
    --bg-secondary: #161b22;
    --bg-tertiary: #1c2333;
    --accent: #58a6ff;
    --accent-glow: rgba(88,166,255,0.25);
    --text-primary: #e6edf3;
    --text-secondary: #8b949e;
    --border: #30363d;
    --success: #3fb950;
    --gradient-start: #7c3aed;
    --gradient-end: #2563eb;
}

.stApp {
    background: var(--bg-primary) !important;
    font-family: 'Inter', sans-serif;
}

/* ─── Header ─── */
.nova-header {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.nova-header h1 {
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--gradient-start), var(--accent), var(--gradient-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
    letter-spacing: -0.5px;
}
.nova-header p {
    color: var(--text-secondary);
    font-size: 1rem;
    margin: 0;
}

/* ─── Chat bubbles ─── */
.chat-container {
    max-width: 760px;
    margin: 0 auto;
    padding: 0 1rem;
}
.user-msg, .bot-msg {
    padding: 1rem 1.25rem;
    border-radius: 14px;
    margin-bottom: 1rem;
    font-size: 0.95rem;
    line-height: 1.65;
    animation: fadeSlideIn 0.35s ease-out;
}
.user-msg {
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
    color: #fff;
    margin-left: 15%;
    border-bottom-right-radius: 4px;
    font-family: 'Inter', sans-serif;
}
.bot-msg {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border);
    margin-right: 10%;
    border-bottom-left-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    white-space: pre-wrap;
    box-shadow: 0 0 20px rgba(0,0,0,0.25);
}
.bot-msg .label {
    color: var(--success);
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 6px;
}
.bot-msg .label::before {
    content: '▸';
    color: var(--success);
}

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ─── Input area ─── */
.stTextArea textarea {
    background: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}
.stTextArea label {
    color: var(--text-secondary) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}

/* ─── Buttons ─── */
.stButton > button {
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px;
    transition: transform 0.15s, box-shadow 0.2s !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(124,58,237,0.5) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ─── Spinner ─── */
.stSpinner > div {
    border-top-color: var(--accent) !important;
}
.stSpinner > div > span {
    color: var(--text-secondary) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ─── Divider ─── */
hr {
    border-color: var(--border) !important;
    opacity: 0.5;
}

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-secondary); }

/* ─── Status badge ─── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--bg-tertiary);
    padding: 0.35rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    color: var(--text-secondary);
    border: 1px solid var(--border);
    margin-top: 0.5rem;
}
.status-badge .dot {
    width: 7px; height: 7px;
    background: var(--success);
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* Hide default Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────
st.markdown("""
<div class="nova-header">
    <h1>🚀 NovaChat</h1>
    <p>AI-powered Policy Assistant &nbsp;·&nbsp; Paste your query below</p>
    <div style="display:flex;justify-content:center;margin-top:0.75rem;">
        <div class="status-badge">
            <span class="dot"></span>
            Local RAG Pipeline &nbsp;·&nbsp; Online
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Session state for chat history ───────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Render chat history ─────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-msg">{msg["content"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="bot-msg"><div class="label">NovaChat Response</div>{msg["content"]}</div>',
            unsafe_allow_html=True,
        )

# ── Input area ───────────────────────────────────────────────────────
with st.container():
    user_input = st.text_area(
        "📋  Paste your input here",
        height=120,
        placeholder="Type or paste your question here...\nFor example: What is the leave policy?",
        key="query_input",
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        send = st.button("⚡ Send Query", use_container_width=True)
    with col3:
        clear = st.button("🗑️ Clear Chat", use_container_width=True)

# ── Clear chat ───────────────────────────────────────────────────────
if clear:
    st.session_state.messages = []
    st.rerun()

# ── Process query ────────────────────────────────────────────────────
if send and user_input.strip():
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    st.markdown(
        f'<div class="user-msg">{user_input.strip()}</div>',
        unsafe_allow_html=True,
    )

    # Get answer from the retrieval pipeline
    with st.spinner("🔍 Querying the knowledge base..."):
        try:
            answer = main(user_input.strip())
        except Exception as e:
            answer = f"❌ Error: {e}"

    # Save bot response
    st.session_state.messages.append({"role": "bot", "content": answer})

    # Simulate terminal-style streaming output
    placeholder = st.empty()
    streamed = ""
    for char in answer:
        streamed += char
        placeholder.markdown(
            f'<div class="bot-msg"><div class="label">NovaChat Response</div>{streamed}▌</div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.008)  # typing speed

    # Final render without cursor
    placeholder.markdown(
        f'<div class="bot-msg"><div class="label">NovaChat Response</div>{streamed}</div>',
        unsafe_allow_html=True,
    )
