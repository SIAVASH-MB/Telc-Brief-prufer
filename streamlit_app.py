import streamlit as st
from openai import OpenAI
import prompts
import random
try:
    from grader import grade_text, GradingResult  # Import from your grader module
except ImportError:
    st.error("grader.py not found. Please ensure it is in the same directory.")
    st.stop()

st.set_page_config(page_title="German Text Grader", page_icon="📝")
st.title("🇩🇪 German Text Grader (telc Style)")

# --- API Key Handling ---
# Priority: 1. Streamlit Secrets, 2. Sidebar Input
api_key = None
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    api_key = st.sidebar.text_input("OPENAI_API_KEY", type="password")

if not api_key:
    st.warning("Please provide an OpenAI API key in the sidebar to proceed (or set it in .streamlit/secrets.toml).")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Configuration")
    level = st.selectbox("Select Target Level", ["B1", "B2"], index=0)

# --- Session State for Topic ---
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = None

# --- Exam Simulation Section ---
st.header("1. Exam Simulation (Topic Generation)")
st.caption("Generate a random exam topic to practice writing tailored to a specific scenario.")

if st.button("Generate Random Topic"):
    # Filter topics by level if implemented, currently only B1 topics available in prompts.B1_TOPICS
    if level == "B1":
        topic = random.choice(prompts.B1_TOPICS)
        st.session_state.current_topic = topic
    else:
        st.info("Topic generation strictly implemented for B1 at the moment. Using standard grading for B2.")
        st.session_state.current_topic = None

if st.session_state.current_topic:
    topic = st.session_state.current_topic
    st.info(f"**Subject:** {topic['subject']}")
    st.write(f"**Situation:** {topic['description']}")
    st.write("**Guiding Points:**")
    for point in topic['points']:
        st.write(f"- {point}")
else:
    if level == "B1":
        st.write("Click the button above to generate a practice topic.")

# --- Text Input Section ---
st.header("2. Your Text")
text = st.text_area("Write your letter/email here:", height=300)

# --- Grading Section ---
if st.button("Grade Text"):
    if not api_key:
        st.error("No API Key provided.")
    elif not text:
        st.warning("Please enter some text to grade.")
    else:
        with st.spinner("Grading... Please wait..."):
            try:
                client = OpenAI(api_key=api_key)
                
                # Pass the topic to the grader if it exists and level is B1
                grading_topic = st.session_state.current_topic if level == "B1" else None
                
                result = grade_text(client, text, level, topic=grading_topic)

                # --- Display Results ---
                st.divider()
                st.header(f"Results ({level})")
                
                # Total Score
                score_color = "red"
                if result.total_score >= 35: score_color = "green"
                elif result.total_score >= 20: score_color = "orange"
                
                st.markdown(f"### Total Score: :{score_color}[{result.total_score} / 45]")
                st.caption(result.total_score_explanation)

                # Detailed Scores Table
                scores_data = {
                    "Criterion": ["Task Management", "Communicative Design", "Formal Correctness"],
                    "Score": [
                        result.criteria_scores.task_management.score,
                        result.criteria_scores.communicative_design.score,
                        result.criteria_scores.formal_correctness.score
                    ],
                    "Reason": [
                        result.criteria_scores.task_management.reason,
                        result.criteria_scores.communicative_design.reason,
                        result.criteria_scores.formal_correctness.reason
                    ]
                }
                st.table(scores_data)

                # Interactive Corrections
                if result.corrections:
                    st.subheader("Detail Corrections")
                    for corr in result.corrections:
                        with st.expander(f"{corr.type}: \"{corr.original}\" -> \"{corr.correction}\""):
                            st.write(f"**Explanation:** {corr.explanation}")

                # General Output
                st.subheader("General Feedback")
                st.info(result.general_feedback)

                st.subheader("Improved Version (Model Answer)")
                st.success(result.improved_version)

            except Exception as e:
                st.error(f"An error occurred during grading: {e}")
