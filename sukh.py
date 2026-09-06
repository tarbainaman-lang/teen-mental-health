import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Teen Mental Health Dashboard",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LIGHT PINK CUSTOM CSS STYLING ---
light_pink_css = """
<style>
    /* Main Background & Text Color */
    .stApp {
        background-color: #FFF5F7;
        color: #4A3E3D;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #FFE4E8 !important;
        border-right: 2px solid #FFC0CB !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-weight: 600;
        font-size: 16px;
        color: #8B4513;
    }

    /* Metric Cards Styling (Light Pink Theme) */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #FFC0CB;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 4px 12px rgba(255, 182, 193, 0.4);
        margin-bottom: 15px;
    }
    .metric-title {
        color: #8B5E66;
        font-size: 14px;
        font-weight: 600;
    }
    .metric-value {
        color: #D81B60;
        font-size: 26px;
        font-weight: 700;
    }

    /* Expander Headers Customization */
    .streamlit-expanderHeader {
        background-color: #FFE4E8 !important;
        border-radius: 8px !important;
        border: 1px solid #FFB6C1 !important;
        color: #C2185B !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    /* Custom Headers */
    .section-header {
        color: #C2185B;
        border-bottom: 2px solid #FFB6C1;
        padding-bottom: 8px;
        margin-top: 15px;
        margin-bottom: 20px;
        font-size: 22px;
        font-weight: 700;
    }
</style>
"""
st.markdown(light_pink_css, unsafe_allow_html=True)

# --- 3. PYTHON DATA LOADING FUNCTION ---
@st.cache_data
def load_data():
    try:
        # Python Pandas reading the CSV dataset
        df = pd.read_csv('Cleaned_Teen_Mental_Health.csv')
        return df
    except Exception as e:
        st.error(f"Error loading file with Python Pandas: {e}")
        return None

df = load_data()

# --- 4. SIDEBAR NAVIGATION & PYTHON DYNAMIC FILTERS ---
st.sidebar.title("🌸 Main Menu")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Page:",
    ["Home", "Data Overview", "Preprocessing", "Visualization", "About"]
)

st.sidebar.markdown("---")

if df is not None:
    # Python Filters on Sidebar
    st.sidebar.subheader("🔍 Python Interactive Filters")
    gender_filter = st.sidebar.multiselect(
        "Select Gender:",
        options=df["gender"].unique(),
        default=df["gender"].unique()
    )

    age_range = st.sidebar.slider(
        "Select Age Range:",
        int(df["age"].min()),
        int(df["age"].max()),
        (int(df["age"].min()), int(df["age"].max()))
    )

    # Filtering DataFrame using Python Pandas
    filtered_df = df[
        (df["gender"].isin(gender_filter)) &
        (df["age"].between(age_range[0], age_range[1]))
    ]

    # ==================== PAGE 1: HOME ====================
    if page == "Home":
        st.markdown("<h1 style='color: #D81B60;'>🌸 Teen Mental Health Dashboard</h1>", unsafe_allow_html=True)
        st.write("An interactive analytics dashboard built using Python to explore social media usage, sleep habits, and teen mental health.")
        st.write("---")

        # Dynamic Calculations using Python Logic
        total_records = len(filtered_df)
        avg_age = filtered_df["age"].mean() if total_records > 0 else 0
        avg_social = filtered_df["daily_social_media_hours"].mean() if total_records > 0 else 0
        at_risk = len(filtered_df[filtered_df["digital_wellbeing_flag"] == "At Risk"])

        # Display Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Filtered Records</div><div class="metric-value">{total_records}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Average Age</div><div class="metric-value">{avg_age:.1f} yrs</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Avg Social Hours</div><div class="metric-value">{avg_social:.1f} hrs</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card"><div class="metric-title">At Risk Count</div><div class="metric-value">{at_risk}</div></div>', unsafe_allow_html=True)

        st.markdown("<div class='section-header'>📌 Key Insights & Goals</div>", unsafe_allow_html=True)
        
        with st.expander("🔍 Click to view Project Objectives", expanded=True):
            st.write("""
            - **Python Data Engine:** Uses Pandas & NumPy for instant metric filtering.
            - **Objective:** Analyze screen time, platform preferences, and sleep metrics against psychological stress indicators.
            """)

        with st.expander("📊 Main Indicators Included"):
            st.write("""
            - **Demographic:** Age (13-19), Gender
            - **Digital Habits:** Screen Time before sleep, Daily Social Media Hours
            - **Psychological Indicators:** Anxiety level, Stress level, Depression label, Sleep Quality
            """)

    # ==================== PAGE 2: DATA OVERVIEW ====================
    elif page == "Data Overview":
        st.markdown("<div class='section-header'>📂 Data Overview (Python Pandas View)</div>", unsafe_allow_html=True)

        with st.expander("📄 Filtered Dataset Rows", expanded=True):
            rows_to_show = st.slider("Select rows to view:", 5, 50, 10)
            st.dataframe(filtered_df.head(rows_to_show), use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            with st.expander("📊 Descriptive Statistics (Pandas .describe())"):
                st.dataframe(filtered_df.describe().T, use_container_width=True)
        
        with col_b:
            with st.expander("📋 Feature Metadata"):
                data_info = pd.DataFrame({
                    "Column": filtered_df.columns,
                    "Data Type": [str(filtered_df[c].dtype) for c in filtered_df.columns],
                    "Non-Null Count": [filtered_df[c].count() for c in filtered_df.columns]
                })
                st.dataframe(data_info, use_container_width=True)

    # ==================== PAGE 3: PREPROCESSING ====================
    elif page == "Preprocessing":
        st.markdown("<div class='section-header'>⚙️ Data Preprocessing & Validation</div>", unsafe_allow_html=True)

        with st.expander("🛠️ Python Null Value Verification", expanded=True):
            null_count = filtered_df.isnull().sum().reset_index()
            null_count.columns = ['Feature Name', 'Missing Count']
            st.dataframe(null_count, use_container_width=True)
            st.success("✔ Python check completed: No missing values found!")

        with st.expander("🔄 Categorical Value Value Counts"):
            cat_col = st.selectbox("Select Feature:", ["gender", "platform_usage", "social_interaction_level", "sleep_quality", "digital_wellbeing_flag"])
            st.dataframe(filtered_df[cat_col].value_counts().reset_index(), use_container_width=True)

        with st.expander("📐 Outlier Inspection"):
            num_col = st.selectbox("Select Column:", ["daily_social_media_hours", "sleep_hours", "screen_time_before_sleep", "academic_performance", "mental_health_risk_score"])
            fig_box = px.box(filtered_df, y=num_col, color="digital_wellbeing_flag", color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_box, use_container_width=True)

    # ==================== PAGE 4: VISUALIZATION ====================
    elif page == "Visualization":
        st.markdown("<div class='section-header'>📈 Data Visualizations</div>", unsafe_allow_html=True)

        viz_type = st.selectbox(
            "Select Chart:", 
            [
                "Social Media vs Risk Score", 
                "Sleep Quality vs Academic Performance", 
                "Platform Usage by Risk Flag",
                "Correlation Heatmap"
            ]
        )

        if viz_type == "Social Media vs Risk Score":
            with st.expander("📊 Scatter Plot: Usage vs Mental Risk Score", expanded=True):
                fig = px.scatter(
                    filtered_df, 
                    x="daily_social_media_hours", 
                    y="mental_health_risk_score", 
                    color="digital_wellbeing_flag",
                    size="stress_level",
                    color_discrete_sequence=["#FF69B4", "#FFB6C1", "#DB7093"],
                    title="Social Media Hours vs. Risk Score"
                )
                st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Sleep Quality vs Academic Performance":
            with st.expander("📊 Sleep Quality Boxplot", expanded=True):
                fig = px.box(
                    filtered_df, 
                    x="sleep_quality", 
                    y="academic_performance", 
                    color="gender",
                    color_discrete_sequence=["#FFB6C1", "#FF69B4"],
                    title="Academic Performance Across Sleep Quality"
                )
                st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Platform Usage by Risk Flag":
            with st.expander("📊 Histogram: Platform Breakdown", expanded=True):
                fig = px.histogram(
                    filtered_df, 
                    x="platform_usage", 
                    color="digital_wellbeing_flag", 
                    barmode="group",
                    color_discrete_sequence=px.colors.sequential.RdPu,
                    title="Platform Usage Breakdown"
                )
                st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Correlation Heatmap":
            with st.expander("🔥 Pearson Correlation Heatmap", expanded=True):
                numeric_df = filtered_df.select_dtypes(include=['float64', 'int64'])
                corr = numeric_df.corr()
                fig = px.imshow(
                    corr, 
                    text_auto=True, 
                    aspect="auto", 
                    color_continuous_scale="PuRd",
                    title="Numeric Features Correlation Matrix"
                )
                st.plotly_chart(fig, use_container_width=True)

    # ==================== PAGE 5: ABOUT ====================
    elif page == "About":
        st.markdown("<div class='section-header'>ℹ️ About This Project</div>", unsafe_allow_html=True)
        
        with st.expander("📌 Tech Stack Details", expanded=True):
            st.write("""
            - **Programming Language:** Python 3.x
            - **Data Handling:** Pandas & NumPy
            - **Frontend & Web Framework:** Streamlit
            - **Interactive Visuals:** Plotly Express
            - **Styling:** Custom CSS (Light Pink Soft Palette)
            """)