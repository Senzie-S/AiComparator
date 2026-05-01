import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Import our custom prompts
from prompts import ANALYZE_PROMPT, COMPARE_PROMPT

# ---------------------------------------------------------
# SETUP & CONFIGURATION
# ---------------------------------------------------------

# Load our API key from the .env file
load_dotenv()

# Set up the visual configuration of the page
st.set_page_config(page_title="AI Chained Comparator", page_icon="⚖️", layout="wide")

# Hide the default Streamlit header, menu, and "Deploy" button to make it look like a real app
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Check if the user has added their API key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY or API_KEY == "your_api_key_here":
    st.error("⚠️ Please add your Gemini API Key to the .env file to use this app.")
    st.stop() # Stop running the app if there's no key

# Create the Gemini AI client
client = genai.Client(api_key=API_KEY)

# ---------------------------------------------------------
# CORE LOGIC: THE 3 CHAINED LLM CALLS
# ---------------------------------------------------------

def step_1_analyze_item_a(item_text):
    """Call 1: Ask Gemini to analyze the first item."""
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Please analyze this item:\n\n{item_text}",
        config=types.GenerateContentConfig(
            system_instruction=ANALYZE_PROMPT,
            temperature=0.5, # Keep it factual
        )
    )
    return response.text

def step_2_analyze_item_b(item_text):
    """Call 2: Ask Gemini to analyze the second item."""
    # We use the exact same logic as Step 1, but for the second item
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Please analyze this item:\n\n{item_text}",
        config=types.GenerateContentConfig(
            system_instruction=ANALYZE_PROMPT,
            temperature=0.5,
        )
    )
    return response.text

def step_3_compare_them(analysis_a, analysis_b):
    """Call 3: Pass BOTH previous analyses to Gemini and ask for a verdict."""
    combined_context = f"""
    Here is the analysis for Item A:
    {analysis_a}
    
    -------------------
    
    Here is the analysis for Item B:
    {analysis_b}
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=combined_context,
        config=types.GenerateContentConfig(
            system_instruction=COMPARE_PROMPT,
            temperature=0.7, # Slightly more creative for the verdict
        )
    )
    return response.text


# ---------------------------------------------------------
# USER INTERFACE (FRONTEND)
# ---------------------------------------------------------

st.title("⚖️ The Ultimate AI Comparator")
st.markdown("Paste two things below (Job Descriptions, Technologies, React vs Vue, etc.).")
st.markdown("**This app makes 3 separate LLM calls to analyze and compare them!**")

# Create two columns side-by-side for the user to type into
col_left, col_right = st.columns(2)

with col_left:
    item_a_input = st.text_area("Item A (Paste text or name)", height=150, placeholder="e.g. React.js")

with col_right:
    item_b_input = st.text_area("Item B (Paste text or name)", height=150, placeholder="e.g. Vue.js")

# When the user clicks the giant button
if st.button("Analyze & Compare! 🚀", use_container_width=True):
    
    if not item_a_input or not item_b_input:
        st.warning("Please fill out both Item A and Item B!")
    else:
        # Create a visual separator
        st.divider()
        st.subheader("Processing Chained LLM Calls...")
        
        # Create 3 columns to show the progress and results of our 3 calls side-by-side
        result_col1, result_col2, result_col3 = st.columns(3)
        
        # --- CALL 1 ---
        with result_col1:
            with st.spinner("Call 1: Analyzing Item A..."):
                analysis_a = step_1_analyze_item_a(item_a_input)
                st.success("✅ Item A Analyzed")
                with st.expander("See Item A Analysis"):
                    st.markdown(analysis_a)

        # --- CALL 2 ---
        with result_col2:
            with st.spinner("Call 2: Analyzing Item B..."):
                analysis_b = step_2_analyze_item_b(item_b_input)
                st.success("✅ Item B Analyzed")
                with st.expander("See Item B Analysis"):
                    st.markdown(analysis_b)

        # --- CALL 3 ---
        with result_col3:
            with st.spinner("Call 3: Generating Final Verdict..."):
                # Notice how we pass the OUTPUTS of Call 1 and Call 2 into Call 3!
                final_verdict = step_3_compare_them(analysis_a, analysis_b)
                st.success("✅ Final Verdict Ready!")
                
        # Show the final verdict big and bold at the bottom
        st.divider()
        st.header("🏆 The Final Verdict")
        st.info("This verdict was generated by taking the results of Call 1 and Call 2 and chaining them into a 3rd prompt.")
        st.markdown(final_verdict)
