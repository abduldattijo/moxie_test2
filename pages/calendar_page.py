import streamlit as st
from utils.calendar_integration import milestone_calendar_ui
# Change this:


# To this:
from utils.state_management import reset_form

def display_calendar():
    """Display calendar scheduling interface"""
    plan = st.session_state.generated_plan
    
    if not plan:
        st.error("Something went wrong. Please try again.")
        if st.button("Start Over"):
            reset_form()
        return
    
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<div class="result-header">', unsafe_allow_html=True)
    st.markdown('<h2>Schedule Your Launch Milestones</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display summary of the plan
    st.markdown('<div class="summary-box">', unsafe_allow_html=True)
    st.markdown(f"<p><strong>{plan['startup_name']}</strong> - {plan['launch_summary']['launch_type']} ({plan['launch_summary']['funding_status']})</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Calendar UI
    milestone_calendar_ui(st.session_state.form_data['email'], plan)
    
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("← Back to Launch Plan", use_container_width=True):
            st.session_state.show_calendar = False
            st.experimental_rerun()
    
    with col2:
        if st.button("Continue", use_container_width=True):
            st.session_state.show_calendar = False
            st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)