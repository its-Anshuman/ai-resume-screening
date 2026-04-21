import streamlit as st
import pandas as pd
from main import run_pipeline

st.set_page_config(page_title="AI Resume Screening", layout="wide")

st.title("🚀 AI Resume Screening & Referral System")

# st.markdown("### 📋 How it works:")
# st.markdown("""
# 1. **Enter Job Description** in the text area below
# 2. **Click "Run Screening"** to process all resumes from Google Sheets
# 3. **Filter results** by category (Shortlist/Maybe/Reject)
# 4. **Download results** as CSV for further analysis
# """)

# st.markdown("---")
st.markdown("### Paste Job Description")

jd = st.text_area(
    "Job Description",
    height=200,
    placeholder="Enter job description here..."
)

col1, col2, col3 = st.columns(3)

with col1:
    run_btn = st.button("🚀 Run Screening", type="primary")

with col2:
    filter_option = st.selectbox(
        "Filter Candidates",
        ["All", "Shortlist", "Maybe", "Reject"]
    )

# Ensure results key exists in session state
if "results" not in st.session_state:
    st.session_state["results"] = None

with col3:
    if st.session_state.get("results") is not None:
        if st.button("🗑️ Clear Results"):
            st.session_state.results = None
            st.rerun()

if run_btn:
    if not jd.strip():
        st.warning("Please enter a Job Description")
    else:
        try:
            with st.spinner("Processing resumes... ⏳"):
                df = run_pipeline(jd)
                st.session_state.results = df
                st.success(f"✅ Successfully processed {len(df)} candidates!")
        except Exception as e:
            st.error(f"❌ Error processing resumes: {str(e)}")
            st.info("Please check your Google Sheets connection and API keys.")

# Display results
if st.session_state.results is not None:
    df = st.session_state.results.copy()  # Work with a copy

    # Apply filter
    if filter_option != "All":
        df = df[df["Category"] == filter_option]

    st.markdown("### 📊 Candidate Rankings")
    st.markdown(f"**Showing {len(df)} candidates** ({filter_option})")

    st.dataframe(df, use_container_width=True)

    # Add download button for filtered results
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name="resume_screening_results.csv",
        mime="text/csv"
    )

    # Download button
    st.download_button(
        label="📥 Download Results",
        data=df.to_csv(index=False),
        file_name="screened_candidates.csv",
        mime="text/csv"
    )

    # Detailed view
    st.markdown("### 🔍 Candidate Details")

    for i, row in df.iterrows():
        with st.expander(f"{row['Name']} | Score: {row['Score']} | {row['Category']}"):

            st.markdown("**Strengths:**")
            for s in row["Strengths"]:
                st.write(f"- {s}")

            st.markdown("**Weaknesses:**")
            for w in row["Weaknesses"]:
                st.write(f"- {w}")

            st.markdown("**Reasoning:**")
            st.write(row["Reasoning"])