import streamlit as st
from utils.ui_components import display_user_responses_summary, pricing_section
from utils.competitive_analysis import display_competitive_analysis
from utils.email_sender import send_email_to_user
# Change this:


# To this:
from utils.state_management import reset_form

def display_results():
    """Display generated plan and offer email sending"""
    plan = st.session_state.generated_plan
    form_data = st.session_state.form_data
    
    if not plan:
        st.error("Something went wrong. Please try again.")
        if st.button("Start Over"):
            reset_form()
        return
    
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<div class="result-header">', unsafe_allow_html=True)
    st.markdown('<h2>Your High-Impact Launch Plan</h2>', unsafe_allow_html=True)
    st.markdown('<div class="ready-badge">Ready</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display summary box
    st.markdown('<div class="summary-box">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p style="color: #6B7280; font-size: 0.875rem;">Startup</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-weight: 500;">{plan["startup_name"]}</p>', unsafe_allow_html=True)
        
        st.markdown('<p style="color: #6B7280; font-size: 0.875rem;">Funding Status</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-weight: 500;">{plan["launch_summary"]["funding_status"]}</p>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<p style="color: #6B7280; font-size: 0.875rem;">Launch Type</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-weight: 500;">{plan["launch_summary"]["launch_type"]}</p>', unsafe_allow_html=True)
        
        st.markdown('<p style="color: #6B7280; font-size: 0.875rem;">Primary Goal</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-weight: 500;">{plan["launch_summary"]["primary_goal"]}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add user responses summary
    display_user_responses_summary(form_data)
    
    # Messaging advice
    st.markdown(f"**{plan['messaging_advice']}**")
    
    # Display recommended strategies
    st.markdown('<h3 style="font-weight: 600; margin-bottom: 0.5rem;">Recommended Strategies:</h3>', unsafe_allow_html=True)
    for i, strategy in enumerate(plan['recommended_strategies']):
        st.markdown(
            f'<div class="strategy-item">'
            f'<div class="strategy-number">{i+1}</div>'
            f'<span>{strategy}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    
    # Display next steps
    st.markdown('<h3 style="font-weight: 600; margin-bottom: 0.5rem; margin-top: 1.5rem;">Next Steps:</h3>', unsafe_allow_html=True)
    for i, step in enumerate(plan['next_steps']):
        st.markdown(
            f'<div class="strategy-item">'
            f'<div class="next-step-number">{i+1}</div>'
            f'<span>{step}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    
    # Add competitive analysis section
    st.markdown('<div style="margin: 2rem 0; padding-top: 1rem; border-top: 1px solid #E5E7EB;">', unsafe_allow_html=True)
    display_competitive_analysis(
        launch_type=plan['launch_summary']['launch_type'],
        funding_status=plan['launch_summary']['funding_status'],
        selected_industry=form_data['industry']
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Launch Timeline button
    st.markdown('<div style="margin: 1.5rem 0;">', unsafe_allow_html=True)
    if st.button("📅 View & Edit Launch Timeline", use_container_width=True):
        st.session_state.show_calendar = True
        st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display pricing options
    st.markdown('<div style="border-top: 1px solid #E5E7EB; margin-top: 1.5rem; padding-top: 1rem;">', unsafe_allow_html=True)
    st.markdown('<h3 style="font-weight: 600; margin-bottom: 0.75rem;">Ready to execute?</h3>', unsafe_allow_html=True)
    
    pricing_section()
    
    # Email and reset buttons
    st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        if st.button("📧 " + ("Email Sent!" if st.session_state.email_sent else "Send to My Email")):
            with st.spinner("Sending email..."):
                success = send_email_to_user(st.session_state.form_data['email'], plan)
                if success:
                    st.success(f"Your personalized launch plan has been sent to {st.session_state.form_data['email']}!")
                    st.session_state.email_sent = True
                    st.experimental_rerun()
                else:
                    st.error("There was an error sending your email. Please try again.")
    
    with col2:
        if st.button("Reset"):
            reset_form()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close result-card div