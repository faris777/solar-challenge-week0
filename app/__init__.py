import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Load data ---
df_sierra = pd.read_csv('../data/sierraleone_clean.csv')
df_togo = pd.read_csv('../data/togo_clean.csv')
df_benin = pd.read_csv('../data/benin_clean.csv')

# --- Page Config ---
st.set_page_config(page_title="Visualizing Data", layout="wide")
st.title("📊 Visualizing Data")

# --- Sidebar ---
st.sidebar.header("Data from Multiple Countries")
st.sidebar.subheader("Benin, Sierra Leone, and Togo")

selected = st.sidebar.selectbox("Select Country", ["Benin", "Sierra Leone", "Togo"])

# --- Choose dataset based on selection ---
if selected == "Benin":
    df = df_benin
elif selected == "Sierra Leone":
    df = df_sierra
else:
    df = df_togo

# --- Pagination setup ---
ROWS_PER_PAGE = 10
key_name = f"page_{selected.lower().replace(' ', '_')}"

if key_name not in st.session_state:
    st.session_state[key_name] = 0

page_number = st.session_state[key_name]

# --- Data Preview ---
with st.expander(f"🔍 {selected} Data Preview", expanded=True):
    col1, col2, col3 = st.columns([1, 1, 6])
    with col1:
        if st.button("⬅️ Previous", key=f"prev_{selected}") and page_number > 0:
            st.session_state[key_name] -= 1
    with col2:
        if st.button("➡️ Next", key=f"next_{selected}") and (page_number + 1) * ROWS_PER_PAGE < len(df):
            st.session_state[key_name] += 1

    start_idx = st.session_state[key_name] * ROWS_PER_PAGE
    end_idx = start_idx + ROWS_PER_PAGE

    st.write(f"**Page {st.session_state[key_name] + 1} of {len(df) // ROWS_PER_PAGE + 1}**")
    st.dataframe(df.iloc[start_idx:end_idx])

# --- Data Summary ---
with st.expander(f"📈 Data Summary ({selected})", expanded=False):
    st.write(df.describe())

# --- Visualization Section ---
st.markdown("---")
st.subheader(f"📊 Visualizations for {selected}")

col1, col2 = st.columns(2)

# --- Boxplot for GHI, DNI, DHI ---
with col1:
    st.write("### Boxplot of GHI, DNI, DHI")
    fig, ax = plt.subplots(figsize=(6, 4))
    df[["GHI", "DNI", "DHI"]].boxplot(ax=ax)
    ax.set_title(f"{selected} - Distribution of Solar Metrics")
    st.pyplot(fig)

# --- Line plot for GHI over Time ---
with col2:
    st.write("### GHI Trend Over Time")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(df["Timestamp"], df["GHI"], color="tab:blue", label="GHI")
    ax2.set_xlabel("Timestamp")
    ax2.set_ylabel("GHI")
    ax2.set_title(f"{selected} - GHI Over Time")
    plt.xticks(rotation=45)
    st.pyplot(fig2)
