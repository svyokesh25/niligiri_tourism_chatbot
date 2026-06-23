import streamlit as st
import json
from google import genai

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ooty Explorer",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@300;400;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    color: #2c2c2c;
}

.stApp {
    background-color: #f6f3ee;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #1a3a2a 0%, #2d5a3d 60%, #3d7a52 100%);
    border-right: none;
}

[data-testid="stSidebar"] * {
    color: #e8f5e2 !important;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #a8d5a2 !important;
    font-family: 'Playfair Display', serif !important;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1a3a2a 0%, #2d5a3d 50%, #4a7c59 100%);
    border-radius: 16px;
    padding: 48px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(26,58,42,0.18);
}

.hero-banner::before {
    content: "🌿";
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 96px;
    opacity: 0.15;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: #e8f5e2;
    margin: 0 0 8px 0;
    line-height: 1.15;
}

.hero-subtitle {
    font-size: 1.15rem;
    color: #a8d5a2;
    font-weight: 300;
    letter-spacing: 0.04em;
    margin: 0;
}

.hero-tagline {
    display: inline-block;
    background: rgba(168,213,162,0.18);
    border: 1px solid rgba(168,213,162,0.4);
    color: #c8e8c2;
    font-size: 0.82rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 16px;
    font-weight: 600;
}

/* ── Chat container ── */
.chat-wrapper {
    background: #ffffff;
    border-radius: 16px;
    border: 1px solid #e0dbd2;
    box-shadow: 0 2px 16px rgba(44,44,44,0.06);
    overflow: hidden;
    margin-bottom: 24px;
}

.chat-header {
    background: linear-gradient(90deg, #2d5a3d, #4a7c59);
    padding: 16px 24px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.chat-header-title {
    color: #e8f5e2;
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    font-weight: 700;
    margin: 0;
}

.chat-header-status {
    color: #a8d5a2;
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: #6fcf4a;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    box-shadow: 0 0 6px #6fcf4a;
}

/* ── Messages ── */
.msg-user {
    background: linear-gradient(135deg, #2d5a3d, #3d7a52);
    color: #e8f5e2;
    border-radius: 18px 18px 4px 18px;
    padding: 14px 18px;
    margin: 8px 0 8px 15%;
    font-size: 0.96rem;
    line-height: 1.6;
    box-shadow: 0 2px 8px rgba(45,90,61,0.18);
}

.msg-bot {
    background: #f9f7f3;
    color: #2c2c2c;
    border-radius: 18px 18px 18px 4px;
    padding: 14px 18px;
    margin: 8px 15% 8px 0;
    font-size: 0.96rem;
    line-height: 1.7;
    border: 1px solid #e8e3da;
    box-shadow: 0 2px 8px rgba(44,44,44,0.05);
}

.msg-label-user {
    text-align: right;
    font-size: 0.72rem;
    color: #7a9e82;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
    font-weight: 600;
}

.msg-label-bot {
    font-size: 0.72rem;
    color: #9e9688;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
    font-weight: 600;
}

/* ── Input area ── */
.input-area {
    background: #faf8f5;
    border-top: 1px solid #e0dbd2;
    padding: 20px 24px;
}

/* ── Quick-select chips ── */
.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 20px;
}

.chip {
    background: #eef6eb;
    border: 1px solid #b8d8b0;
    color: #2d5a3d;
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 600;
    letter-spacing: 0.02em;
}

.chip:hover {
    background: #2d5a3d;
    color: #e8f5e2;
    border-color: #2d5a3d;
}

/* ── Streamlit overrides ── */
.stTextInput > div > div > input {
    border: 1.5px solid #c8d8c0 !important;
    border-radius: 10px !important;
    background: #ffffff !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 0.96rem !important;
    padding: 10px 16px !important;
    color: #2c2c2c !important;
    box-shadow: 0 1px 4px rgba(44,44,44,0.06) !important;
    transition: border-color 0.2s !important;
}

.stTextInput > div > div > input:focus {
    border-color: #2d5a3d !important;
    box-shadow: 0 0 0 3px rgba(45,90,61,0.12) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #2d5a3d, #4a7c59) !important;
    color: #e8f5e2 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    padding: 10px 24px !important;
    font-size: 0.92rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 8px rgba(45,90,61,0.22) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1a3a2a, #2d5a3d) !important;
    box-shadow: 0 4px 16px rgba(45,90,61,0.32) !important;
    transform: translateY(-1px) !important;
}

/* Clear button style */
.clear-btn > button {
    background: transparent !important;
    color: #9e9688 !important;
    border: 1px solid #d0c9be !important;
    box-shadow: none !important;
    font-size: 0.82rem !important;
    padding: 8px 16px !important;
}

.clear-btn > button:hover {
    background: #f0ece5 !important;
    color: #5a5248 !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #2d5a3d !important;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #e0dbd2;
    margin: 24px 0;
}

/* Scrollable chat area */
.scrollable-chat {
    max-height: 480px;
    overflow-y: auto;
    padding: 24px;
    scrollbar-width: thin;
    scrollbar-color: #c8d8c0 #f6f3ee;
}

.scrollable-chat::-webkit-scrollbar {
    width: 5px;
}
.scrollable-chat::-webkit-scrollbar-track {
    background: #f6f3ee;
}
.scrollable-chat::-webkit-scrollbar-thumb {
    background: #c8d8c0;
    border-radius: 4px;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 48px 24px;
    color: #9e9688;
}

.empty-state-icon {
    font-size: 56px;
    margin-bottom: 16px;
    display: block;
}

.empty-state-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #5a7a62;
    margin-bottom: 8px;
}

.empty-state-sub {
    font-size: 0.9rem;
    line-height: 1.6;
}

/* Info cards in sidebar */
.info-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(168,213,162,0.25);
    border-radius: 10px;
    padding: 14px;
    margin-bottom: 12px;
}

.info-card-title {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #a8d5a2 !important;
    font-weight: 600;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)


# ── Load data & init client ────────────────────────────────────────────────────

@st.cache_data
def load_data():
    # TODO: Replace with your actual JSON file path
    with open("nilgiris_tourism_100_plus.json", "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_resource
def get_client():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("❌ API key not found! Please add GOOGLE_API_KEY to .streamlit/secrets.toml")
        st.stop()
    return genai.Client(api_key=api_key)


SYSTEM_PROMPT = """
# Ooty Tourist Places Chatbot - System Prompt

You are "Ooty Explorer", an AI assistant that helps users discover tourist attractions in Ooty and the Nilgiris district of Tamil Nadu, India.

Your expertise is limited to tourist places and sightseeing recommendations.

You have access to a knowledge base containing information about:
* Tourist attractions, Lakes, Waterfalls, Viewpoints, Gardens, Museums, Tea estates, Heritage sites, Wildlife destinations, Trekking spots

Your coverage includes: Ooty, Coonoor, Kotagiri, Gudalur, Masinagudi, Mudumalai, Avalanche, Emerald

## Instructions
* Answer questions only using the retrieved information from the knowledge base.
* Never make up facts, timings, fees, distances, or travel details.
* If information is unavailable, say: "I don't have verified information about that place."
* If a user asks about hotels, restaurants, shopping, weather, transport, or topics unrelated to tourist attractions, politely explain that you specialize only in tourist places in the Nilgiris district.
* Keep responses short, clear, and useful.
* Use bullet points whenever possible.
* When describing a place, include: Name, Category, Location, Short description, Highlights, Best time to visit, Recommended visit duration
* If users ask for recommendations, suggest places based on their interests:
  - Families → gardens, lakes, toy train
  - Couples → viewpoints, lakes, tea estates
  - Adventure lovers → trekking spots, waterfalls, wildlife areas
  - Photography enthusiasts → viewpoints, tea plantations, sunrise locations
* Recommend nearby attractions when relevant.
* If multiple places match a request, rank them by popularity and relevance.

## Response Format
Place Name:
Category:
Location:
Description:
Highlights:
Best Time to Visit:
Recommended Duration:
Nearby Attractions:

Always prioritize accuracy over completeness.
You should answer politely. If there is any question outside your data say "I don't have verified information about that place."
Only refer to data and provide response.

# Additional Knowledge Base — Nilgiris Tourism Master File

## Government Botanical Garden
Category: Garden | Distance from Ooty Bus Stand: 2 km | Established: 1848
Famous for: One of India's oldest botanical gardens; annual flower show
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Ooty Lake
Category: Lake | Distance from Ooty Bus Stand: 3 km | Established: 1824
Famous for: Artificial lake famous for boating and family activities
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Doddabetta Peak
Category: Viewpoint | Distance from Ooty Bus Stand: 10 km | Established: Natural attraction
Famous for: Highest peak in Tamil Nadu with panoramic views
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Government Rose Garden
Category: Garden | Distance from Ooty Bus Stand: 4 km | Established: 1995
Famous for: One of India's largest rose gardens
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Nilgiri Mountain Railway
Category: Heritage Railway | Distance from Ooty Bus Stand: 1 km | Established: 1908
Famous for: UNESCO World Heritage toy train
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Tea Museum and Factory
Category: Museum | Distance from Ooty Bus Stand: 4 km
Famous for: Tea processing demonstrations and tastings
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Pykara Lake
Category: Lake | Distance from Ooty Bus Stand: 21 km | Established: Natural attraction
Famous for: Boating and scenic pine forests
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Pykara Falls
Category: Waterfall | Distance from Ooty Bus Stand: 23 km | Established: Natural attraction
Famous for: Twin waterfalls surrounded by forests
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Avalanche Lake
Category: Lake | Distance from Ooty Bus Stand: 28 km | Established: Natural attraction
Famous for: Pristine lake with trekking and camping
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Emerald Lake
Category: Lake | Distance from Ooty Bus Stand: 25 km | Established: Natural attraction
Famous for: Peaceful lake amid tea estates
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Pine Forest
Category: Forest | Distance from Ooty Bus Stand: 15 km
Famous for: Popular film shooting location
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Thread Garden
Category: Museum | Distance from Ooty Bus Stand: 3 km | Established: 2001
Famous for: Artificial flowers made entirely from thread
Best Time to Visit: October to May | Duration: 1 to 3 hours

## St. Stephen's Church
Category: Heritage Site | Distance from Ooty Bus Stand: 2 km | Established: 1830
Famous for: Colonial church with stained-glass windows
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Mukurthi National Park
Category: Wildlife | Distance from Ooty Bus Stand: 34 km | Established: 1990
Famous for: UNESCO Biosphere Reserve habitat
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Ketti Valley View
Category: Viewpoint | Distance from Ooty Bus Stand: 8 km | Established: Natural attraction
Famous for: One of the world's largest inhabited valleys
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Tiger Hill
Category: Viewpoint | Distance from Ooty Bus Stand: 6 km | Established: Natural attraction
Famous for: Sunrise views over Ooty
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Wenlock Downs
Category: Grassland | Distance from Ooty Bus Stand: 17 km | Established: Natural attraction
Famous for: Rolling meadows and film location
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Upper Bhavani Lake
Category: Lake | Distance from Ooty Bus Stand: 38 km | Established: Natural attraction
Famous for: Remote reservoir with forest views
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Glenmorgan Tea Estate
Category: Tea Estate | Distance from Ooty Bus Stand: 25 km | Established: 1920s
Famous for: Historic tea plantation and viewpoints
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Kamraj Sagar Dam
Category: Reservoir | Distance from Ooty Bus Stand: 10 km | Established: 1950s
Famous for: Picnic spot and birdwatching
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Sim's Park
Category: Garden | Distance from Ooty Bus Stand: 20 km (Coonoor) | Established: 1874
Famous for: Botanical park in Coonoor
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Dolphin's Nose
Category: Viewpoint | Distance from Ooty Bus Stand: 30 km | Established: Natural attraction
Famous for: Spectacular cliffside views
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Lamb's Rock
Category: Viewpoint | Distance from Ooty Bus Stand: 28 km | Established: Natural attraction
Famous for: Views of tea estates and plains
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Catherine Falls
Category: Waterfall | Distance from Ooty Bus Stand: 35 km | Established: Natural attraction
Famous for: Double-cascaded waterfall
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Laws Falls
Category: Waterfall | Distance from Ooty Bus Stand: 26 km | Established: Natural attraction
Famous for: Monsoon-fed waterfall
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Kodanad View Point
Category: Viewpoint | Distance from Ooty Bus Stand: 33 km | Established: Natural attraction
Famous for: Views of Moyar Valley
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Longwood Shola
Category: Forest | Distance from Ooty Bus Stand: 32 km
Famous for: Rare shola ecosystem
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Needle Rock View Point
Category: Viewpoint | Distance from Ooty Bus Stand: 51 km | Established: Natural attraction
Famous for: 360-degree valley views
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Mudumalai Tiger Reserve
Category: Wildlife | Distance from Ooty Bus Stand: 42 km | Established: 1940
Famous for: Elephant safaris and wildlife
Best Time to Visit: October to May | Duration: 1 to 3 hours

## Theppakadu Elephant Camp
Category: Wildlife | Distance from Ooty Bus Stand: 44 km | Established: 1972
Famous for: One of Asia's oldest elephant camps
Best Time to Visit: October to May | Duration: 1 to 3 hours

{data}
"""

QUICK_PROMPTS = [
    "🏔️ Best viewpoints in Ooty",
    "🌊 Waterfalls near Coonoor",
    "🌿 Tea estate tours",
    "🦁 Wildlife in Mudumalai",
    "👨‍👩‍👧 Family-friendly spots",
    "📸 Photography locations",
    "🥾 Trekking spots",
    "🌸 Best time to visit Ooty",
]


# ── Sidebar ────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 8px 0 24px 0;">
        <div style="font-size:52px; margin-bottom:10px;">🌿</div>
        <div style="font-family:'Playfair Display',serif; font-size:1.5rem; font-weight:700; color:#e8f5e2;">Ooty Explorer</div>
        <div style="font-size:0.78rem; color:#a8d5a2; letter-spacing:0.1em; text-transform:uppercase; margin-top:4px;">Nilgiris Tourism Guide</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📍 Coverage Areas")
    areas = ["Ooty", "Coonoor", "Kotagiri", "Gudalur", "Masinagudi", "Mudumalai", "Avalanche", "Emerald"]
    for area in areas:
        st.markdown(f"<div style='padding:4px 0; color:#c8e8c2; font-size:0.9rem;'>▸ {area}</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🗂️ What I Know")
    categories = [
        ("🏞️", "Viewpoints & Peaks"),
        ("🌊", "Waterfalls"),
        ("🌿", "Tea Estates"),
        ("🌸", "Gardens & Parks"),
        ("🦁", "Wildlife Sanctuaries"),
        ("🏛️", "Heritage Sites"),
        ("🥾", "Trekking Trails"),
        ("💧", "Lakes"),
    ]
    for icon, cat in categories:
        st.markdown(f"<div style='padding:5px 0; color:#c8e8c2; font-size:0.88rem;'>{icon} {cat}</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style="font-size:0.75rem; color:#7aaa82; text-align:center; line-height:1.7; padding-top:4px;">
        Powered by Gemini 2.5 Flash<br>
        <span style="opacity:0.6;">Tamil Nadu Tourism Data</span>
    </div>
    """, unsafe_allow_html=True)


# ── Main content ───────────────────────────────────────────────────────────────

# Hero banner
st.markdown("""
<div class="hero-banner">
    <div class="hero-tagline">🌿 Nilgiris District · Tamil Nadu</div>
    <div class="hero-title">Discover Ooty & Beyond</div>
    <div class="hero-subtitle">Your personal guide to the Blue Mountains — viewpoints, waterfalls, tea estates & more</div>
</div>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    try:
        data = load_data()
        client = get_client()
        prompt_with_data = SYSTEM_PROMPT.replace("{data}", json.dumps(data, ensure_ascii=False))
        st.session_state.chat = client.chats.create(
            model="gemini-2.5-flash",
            config={"system_instruction": prompt_with_data}
        )
        st.session_state.data_loaded = True
    except FileNotFoundError:
        st.session_state.data_loaded = False
        st.error("⚠️ `nilgiris_tourism_100_plus.json` not found. Place it in the same directory as this script.")
    except Exception as e:
        st.session_state.data_loaded = False
        st.error(f"⚠️ Initialization error: {e}")


# ── Quick prompt chips ─────────────────────────────────────────────────────────
st.markdown("**Quick Questions**")

cols = st.columns(4)
for i, qp in enumerate(QUICK_PROMPTS):
    with cols[i % 4]:
        if st.button(qp, key=f"chip_{i}", use_container_width=True):
            st.session_state["pending_input"] = qp.split(" ", 1)[1]  # strip emoji


# ── Chat window ────────────────────────────────────────────────────────────────
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="chat-header">
    <div>
        <span class="status-dot"></span>
    </div>
    <div>
        <div class="chat-header-title">Ooty Explorer Assistant</div>
        <div class="chat-header-status">Online · Ready to guide you</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Messages area
st.markdown('<div class="scrollable-chat">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <span class="empty-state-icon">🌄</span>
        <div class="empty-state-title">Welcome to the Nilgiris!</div>
        <div class="empty-state-sub">Ask me about any tourist place in Ooty, Coonoor, Kotagiri,<br>or anywhere in the Nilgiris district.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-label-user">You</div>
            <div class="msg-user">{msg["content"]}</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-label-bot">🌿 Ooty Explorer</div>
            <div class="msg-bot">{msg["content"]}</div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close scrollable-chat

# Input area
st.markdown('<div class="input-area">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([6, 1, 1])

with col1:
    default_val = st.session_state.pop("pending_input", "")
    user_input = st.text_input(
        label="Ask about tourist places",
        value=default_val,
        placeholder="e.g. Tell me about Doddabetta Peak...",
        label_visibility="collapsed",
        key="user_input_field"
    )

with col2:
    send_clicked = st.button("Send →", use_container_width=True)

with col3:
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("Clear", use_container_width=True):
        st.session_state.messages = []
        if "chat" in st.session_state:
            del st.session_state["chat"]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close input-area
st.markdown('</div>', unsafe_allow_html=True)  # close chat-wrapper


# ── Send message logic ─────────────────────────────────────────────────────────
query = user_input.strip() if send_clicked and user_input.strip() else None

if query and st.session_state.get("data_loaded", False):
    st.session_state.messages.append({"role": "user", "content": query})

    with st.spinner("Exploring the Nilgiris for you..."):
        try:
            response = st.session_state.chat.send_message(query)
            reply = response.text
        except Exception as e:
            reply = f"Sorry, I encountered an error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

elif query and not st.session_state.get("data_loaded", False):
    st.warning("Please fix the initialization errors above before chatting.")


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#9e9688; font-size:0.78rem; margin-top:32px; padding-bottom:16px; letter-spacing:0.04em;">
    🌿 Ooty Explorer &nbsp;·&nbsp; Nilgiris Tourism AI &nbsp;·&nbsp; Powered by Google Gemini
</div>
""", unsafe_allow_html=True)
