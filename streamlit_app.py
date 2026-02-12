import streamlit as st
from openai import OpenAI
import prompts  # Your existing prompts.py

st.set_page_config(page_title="German Text Grader", page_icon="📝")
st.title("🇩🇪 German Text Grader (telc Style)")

# API Key Handling: Priority given to Streamlit Secrets, then user input
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if not api_key and "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]

level = st.selectbox("Select Target Level", ["B1", "B2"])
text = st.text_area("Paste the student's text here:", height=300)

if st.button("Grade Text"):
    if not api_key:
        st.error("Please provide an OpenAI API key in the sidebar.")
    elif not text:
        st.warning("Please enter some text to grade.")
    else:
        with st.spinner("Grading... Please wait..."):
            try:
                client = OpenAI(api_key=api_key)
                # Note: You should move your grade_text logic into a function here
                # or import it if you refactor grader.py to be modular
                result = grade_text(client, text, level)  # Logic from your grader.py

                # Display Results
                st.header(f"Results ({level})")
                st.metric("Total Score", f"{result.total_score} / 45")

                # Scores Table
                scores_data = {
                    "Criterion": ["Task Management", "Communicative Design", "Formal Correctness"],
                    "Score": [result.criteria_scores.task_management.score,
                              result.criteria_scores.communicative_design.score,
                              result.criteria_scores.formal_correctness.score],
                    "Reason": [result.criteria_scores.task_management.reason,
                               result.criteria_scores.communicative_design.reason,
                               result.criteria_scores.formal_correctness.reason]
                }
                st.table(scores_data)

                st.subheader("General Feedback")
                st.info(result.general_feedback)

                st.subheader("Improved Version")
                st.success(result.improved_version)

            except Exception as e:
                st.error(f"Error: {e}")