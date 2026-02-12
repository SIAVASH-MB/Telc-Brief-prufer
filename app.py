import streamlit as st
from openai import OpenAI
import prompts

st.title("German Text Grader (telc Style)")

api_key = st.sidebar.text_input("OpenAI API Key", type="password")
level = st.selectbox("Select Target Level", ["B1", "B2"])
text = st.text_area("Enter the text to grade", height=300)

if st.button("Grade Text"):
    if not api_key:
        st.error("Please enter an API Key.")
    else:
        client = OpenAI(api_key=api_key)
        # Call your grade_text function here...
        # Display results using st.write() and st.table()