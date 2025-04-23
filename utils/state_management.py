import streamlit as st

def reset_form():
    """Reset the form to start over"""
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
    st.session_state.generated_plan = None
    st.session_state.email_sent = False
    st.session_state.show_calendar = False
    st.session_state.step = 1
    st.experimental_rerun()
    