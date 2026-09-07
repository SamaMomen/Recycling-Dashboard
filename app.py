
import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(
    page_title="EcoSort | Smart Recycling",
    page_icon="♻️",
    layout="wide"
)

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #071a14 0%, #0b241c 55%, #102e24 100%);
        color: #f4fff9;
    }
    .block-container { padding-top: 2rem; }
    h1, h2, h3 { color: #f4fff9 !important; }
    .hero {
        padding: 24px 28px;
        border-radius: 22px;
        background: rgba(255,255,255,.07);
        border: 1px solid rgba(255,255,255,.10);
        margin-bottom: 22px;
    }
    .hero small { color: #a9c7bb; font-size: 15px; }
    .card {
        padding: 20px;
        border-radius: 18px;
        background: rgba(255,255,255,.075);
        border: 1px solid rgba(255,255,255,.10);
        min-height: 145px;
    }
    .metric-title { color:#a9c7bb; font-size:14px; }
    .metric-value { font-size:34px; font-weight:800; margin-top:5px; }
    .metric-sub { color:#8ed6b7; font-size:13px; }
    .status {
        padding: 12px 16px;
        border-radius: 14px;
        background: rgba(142,214,183,.12);
        border: 1px solid rgba(142,214,183,.25);
        color: #bff3da;
        text-align:center;
    }
    div.stButton > button {
        width:100%;
        border-radius:14px;
        height:3.2em;
        font-size:18px;
        font-weight:700;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Demo data ----------
data = pd.DataFrame({
    "Type": ["Masks", "Gloves", "Yellow Bags", "Other"],
    "Count": [42, 31, 18, 9]
})
total = int(data["Count"].sum())

# Estimated/entered weights for the prototype
weights = {
    "Masks": 2.4,
    "Gloves": 1.8,
    "Yellow Bags": 8.5,
    "Other": 1.2
}
total_kg = sum(weights.values())

# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>♻️ EcoSort</h1>
    <small>Smart Waste Sorting & Recycling Monitoring System</small>
</div>
""", unsafe_allow_html=True)

# ---------- Metrics ----------
cols = st.columns(5)
metrics = [
    ("😷 Masks", 42, "Detected items"),
    ("🧤 Gloves", 31, "Detected items"),
    ("🟡 Yellow Bags", 18, "Detected bags"),
    ("♻️ Total Waste", total, "Detected items"),
    ("⚖️ Total Weight", f"{total_kg:.1f} kg", "Estimated weight"),
]
for col, (title, value, sub) in zip(cols, metrics):
    with col:
        st.markdown(f"""
        <div class="card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# ---------- Charts ----------
left, right = st.columns([1.15, 1])

with left:
    st.subheader("Waste Composition")
    fig = px.bar(
        data,
        x="Type",
        y="Count",
        text="Count",
        title="Detected Waste by Category"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#f4fff9",
        title_font_color="#f4fff9",
        margin=dict(l=20,r=20,t=55,b=20)
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Distribution")
    fig2 = px.pie(
        data,
        names="Type",
        values="Count",
        hole=.58
    )
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#f4fff9",
        margin=dict(l=10,r=10,t=20,b=10),
        showlegend=True
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------- Recycling ----------
st.divider()
st.subheader("⚖️ Waste Weight")

weight_df = pd.DataFrame({
    "Type": list(weights.keys()),
    "Weight (kg)": list(weights.values())
})
st.dataframe(
    weight_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Weight (kg)": st.column_config.NumberColumn(format="%.1f kg")
    }
)

st.divider()
st.subheader("♻️ Recycling Control")

if "recycling" not in st.session_state:
    st.session_state.recycling = False
if "done" not in st.session_state:
    st.session_state.done = False

if not st.session_state.recycling and not st.session_state.done:
    st.markdown('<div class="status">System ready — waste is waiting to be sorted.</div>', unsafe_allow_html=True)
    st.write("")
    if st.button("♻️ START RECYCLING", type="primary"):
        st.session_state.recycling = True
        st.rerun()

elif st.session_state.recycling:
    st.markdown('<div class="status">🔄 Recycling process in progress...</div>', unsafe_allow_html=True)
    bar = st.progress(0)
    for i in range(101):
        time.sleep(0.015)
        bar.progress(i)
    st.session_state.recycling = False
    st.session_state.done = True
    st.rerun()

else:
    st.success("✅ Recycling completed successfully!")
    result_cols = st.columns(3)
    results = [
        ("😷 Masks", f"{weights['Masks']:.1f} kg"),
        ("🧤 Gloves", f"{weights['Gloves']:.1f} kg"),
        ("🟡 Yellow Bags", f"{weights['Yellow Bags']:.1f} kg")
    ]
    for col, (label, value) in zip(result_cols, results):
        with col:
            st.metric(label, value)

    if st.button("↻ RESET DEMO"):
        st.session_state.done = False
        st.rerun()

st.caption("Prototype / Demo interface — values are sample data and can later be connected to the AI detection model.")
