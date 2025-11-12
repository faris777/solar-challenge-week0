import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# --- Load data ---
df_sierra = pd.read_csv('../data/sierraleone_clean.csv')
df_togo = pd.read_csv('../data/togo_clean.csv')
df_benin = pd.read_csv('../data/benin_clean.csv')

# --- Page Config ---
st.set_page_config(page_title="Visualizing Data", layout="wide")
st.title("📊 Visualizing Data")

# --- Sidebar ---
st.sidebar.header("🌍 Data from Multiple Countries")
st.sidebar.subheader("Benin, Sierra Leone, and Togo")

selected = st.sidebar.selectbox("Select Country", ["Benin", "Sierra Leone", "Togo"])

# --- Filter Controls ---
st.sidebar.markdown("### 🔍 Data Filters")

year_min, year_max = st.sidebar.slider('Select Year Range', 2000, 2020, (2005, 2015))

metric = st.sidebar.radio(
    "Select Metric for Trend Visualization",
    ["GHI", "DNI", "DHI"],
    index=0
)

dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=False)
show_summary = st.sidebar.checkbox("📊 Show Data Summary", value=True)
interactive_mode = st.sidebar.checkbox("⚡ Use Interactive Charts (Plotly)", value=True)

# --- Choose dataset based on selection ---
if selected == "Benin":
    df = df_benin
elif selected == "Sierra Leone":
    df = df_sierra
else:
    df = df_togo

# --- Filter by year range ---
if "Year" in df.columns:
    df = df[(df["Year"] >= year_min) & (df["Year"] <= year_max)]

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

# --- Download filtered data ---
st.sidebar.download_button(
    label="💾 Download Filtered Data (CSV)",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name=f"{selected.lower()}_{year_min}_{year_max}.csv",
    mime='text/csv'
)

# --- Data Summary ---
if show_summary:
    with st.expander(f"📈 Data Summary ({selected})", expanded=False):
        st.write(df.describe())

# --- Visualization Section ---
st.markdown("---")
st.subheader(f"📊 Visualizations for {selected}")

col1, col2 = st.columns(2)

# --- Boxplot (Matplotlib only) ---
with col1:
    st.write("### Boxplot of GHI, DNI, DHI")
    fig, ax = plt.subplots(figsize=(6, 4))
    df[["GHI", "DNI", "DHI"]].boxplot(ax=ax)
    ax.set_title(f"{selected} - Distribution of Solar Metrics")
    if dark_mode:
        fig.patch.set_facecolor('#222')
        ax.set_facecolor('#333')
        ax.title.set_color('white')
        ax.tick_params(colors='white')
    st.pyplot(fig)

# --- Line Plot (Plotly or Matplotlib) ---
with col2:
    st.write(f"### {metric} Trend Over Time")

    if interactive_mode:
        fig2 = px.line(df, x="Timestamp", y=metric, title=f"{selected} - {metric} Over Time", color_discrete_sequence=["blue"])
        fig2.update_layout(template="plotly_dark" if dark_mode else "plotly_white")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.plot(df["Timestamp"], df[metric], color="tab:blue", label=metric)
        ax2.set_xlabel("Timestamp")
        ax2.set_ylabel(metric)
        ax2.set_title(f"{selected} - {metric} Over Time")
        plt.xticks(rotation=45)
        if dark_mode:
            fig2.patch.set_facecolor('#222')
            ax2.set_facecolor('#333')
            ax2.title.set_color('white')
            ax2.tick_params(colors='white')
        st.pyplot(fig2)

# --- Correlation Heatmap ---
st.markdown("---")
st.subheader("📈 Correlation Heatmap")

if interactive_mode:
    corr = df.select_dtypes(include='number').corr()
    fig3 = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu",
        title=f"{selected} - Correlation Matrix"
    )
    fig3.update_layout(template="plotly_dark" if dark_mode else "plotly_white")
    st.plotly_chart(fig3, use_container_width=True)
else:
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax3)
    ax3.set_title(f"{selected} - Correlation Matrix")
    if dark_mode:
        fig3.patch.set_facecolor('#222')
        ax3.set_facecolor('#333')
        ax3.title.set_color('white')
    st.pyplot(fig3)
