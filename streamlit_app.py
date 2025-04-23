import streamlit as st
import os
import json
from datetime import datetime

# Import components
from components.styling import apply_css
from components.header import display_header, display_footer

# Import pages
from pages.form_steps import (
    step_1, step_2, step_3, step_4, step_5, 
    step_6, step_7, step_8, step_9
)
from pages.results_page import display_results
from pages.calendar_page import display_calendar

# Import utilities
from utils.plan_generator import generate_launch_plan
from utils.state_management import reset_form

# Set page configuration
st.set_page_config(
    page_title="Roy",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
apply_css()

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1

if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        'first_name': '',
        'startup_name': '',
        'messaging_tested': None,
        'launch_type': None,
        'funding_status': None,
        'primary_goal': None,
        'audience_readiness': None,
        'post_launch_priority': None,
        'industry': None,
        'email': ''
    }

if 'generated_plan' not in st.session_state:
    st.session_state.generated_plan = None
    
if 'email_sent' not in st.session_state:
    st.session_state.email_sent = False

if 'show_calendar' not in st.session_state:
    st.session_state.show_calendar = False

# Load strategies from JSON file if it exists
def load_strategies():
    try:
        if os.path.exists("data/strategies.json"):
            with open("data/strategies.json", "r") as f:
                return json.load(f)
        return None
    except Exception as e:
        st.error(f"Error loading strategies: {e}")
        return None

# Main app
def main():
    # Display header
    display_header()
    
    # Progress bar (only show if not on results page)
    if st.session_state.generated_plan is None and 1 <= st.session_state.step <= 9:
        progress = (st.session_state.step - 1) / 8
        st.progress(progress)
        st.markdown(f"**Step {st.session_state.step}/9**")
    
    # Route to appropriate page based on state
    if st.session_state.generated_plan is not None:
        if st.session_state.show_calendar:
            display_calendar()
        else:
            display_results()
    elif st.session_state.step == 1:
        step_1()
    elif st.session_state.step == 2:
        step_2()
    elif st.session_state.step == 3:
        step_3()
    elif st.session_state.step == 4:
        step_4()
    elif st.session_state.step == 5:
        step_5()
    elif st.session_state.step == 6:
        step_6()
    elif st.session_state.step == 7:
        step_7()
    elif st.session_state.step == 8:
        step_8()
    elif st.session_state.step == 9:
        step_9()
    
    # Display footer
    display_footer()

if __name__ == "__main__":
    main()