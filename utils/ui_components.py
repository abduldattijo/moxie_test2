import streamlit as st

def option_selector(options, key_prefix, selected_option=None, with_info=False):
    """
    Create a custom radio-button like selector using native radio buttons
    
    Args:
        options (list): List of option labels
        key_prefix (str): Prefix for the key to make it unique
        selected_option (str, optional): Currently selected option
        with_info (bool): Whether this option will show an info box
    
    Returns:
        str: The selected option
    """
    # Find index of selected option
    index = 0
    if selected_option in options:
        index = options.index(selected_option)
    
    # Use native radio buttons with visible labels
    selected = st.radio(
        "",  # Empty label
        options,
        index=index,
        key=f"{key_prefix}_radio",
        label_visibility="collapsed"  # Hide the main label
    )
    
    # Show info box if option is selected and with_info is True
    if with_info and selected:
        display_info_for_option(selected)
    
    return selected

def display_info_for_option(option):
    """Display contextual information based on the selected option"""
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    
    # Launch Type info
    if "New Startup/Product Launch" in option:
        st.markdown(
            'Your first launch moment needs to be more than an announcement. '
            'It\'s a story. Why did you build this? What\'s the problem it solves? '
            'Who will this change everything for?'
        )
    # Add all the other options here as in the original code...
    # ...
    else:
        st.markdown("Select an option to learn more.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def step_navigation(back=True, next_label="Next →", next_disabled=True, on_next=None):
    """
    Create consistent navigation buttons with Back under Next
    
    Args:
        back (bool): Whether to show back button
        next_label (str): Label for the next button
        next_disabled (bool): Whether next button should be disabled
        on_next (function, optional): Function to call on next
    """
    # Create Next button - full width
    if st.button(next_label, disabled=next_disabled, key="next_button", use_container_width=True):
        if on_next:
            on_next()
        else:
            st.session_state.step += 1
            st.experimental_rerun()
    
    # Create Back button below (if needed) - full width
    if back:
        if st.button("← Back", key="back_button", use_container_width=True):
            st.session_state.step -= 1
            st.experimental_rerun()

def step_card(title, content_func):
    """
    Create a styled step card with consistent formatting
    
    Args:
        title (str): Title of the step
        content_func (function): Function that contains the step content
    """
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="step-title">{title}</div>', unsafe_allow_html=True)
    
    # Call the content function
    content_func()
    
    st.markdown('</div>', unsafe_allow_html=True)

def pricing_section():
    """Display the pricing options grid"""
    st.markdown('<div class="pricing-grid">', unsafe_allow_html=True)
    
    # DIY Option
    st.markdown(
        '<div class="pricing-card">'
        '<p class="pricing-title">DIY</p>'
        '<p class="pricing-price">$29/month</p>'
        '<p class="pricing-description">Weekly roadmap</p>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Coaching Option (highlighted)
    st.markdown(
        '<div class="pricing-card highlighted">'
        '<p class="pricing-title">Coaching</p>'
        '<p class="pricing-price">$500/month</p>'
        '<p class="pricing-description">Direct guidance</p>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Full-Service Option
    st.markdown(
        '<div class="pricing-card">'
        '<p class="pricing-title">Full-Service</p>'
        '<p class="pricing-price">$5K</p>'
        '<p class="pricing-description">We run it for you</p>'
        '</div>',
        unsafe_allow_html=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

def info_box(text):
    """Display a consistent info box"""
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown(text)
    st.markdown('</div>', unsafe_allow_html=True)

def display_user_responses_summary(form_data):
    """
    Display a summary of all user responses
    
    Args:
        form_data (dict): User's form data containing all responses
    """
    st.markdown('<h3 style="font-weight: 600; margin-bottom: 0.5rem; margin-top: 1.5rem;">Your Responses</h3>', unsafe_allow_html=True)
    
    # Create an expandable section with all responses
    with st.expander("View all your responses", expanded=False):
        st.markdown("### Messaging Validation")
        st.markdown(f"**Your response:** {form_data['messaging_tested']}")
        
        st.markdown("### Launch Type")
        st.markdown(f"**Your response:** {form_data['launch_type']}")
        
        st.markdown("### Funding Status")
        st.markdown(f"**Your response:** {form_data['funding_status']}")
        
        st.markdown("### Primary Goal")
        st.markdown(f"**Your response:** {form_data['primary_goal']}")
        
        st.markdown("### Audience Readiness")
        st.markdown(f"**Your response:** {form_data['audience_readiness']}")
        
        st.markdown("### Post-Launch Priority")
        st.markdown(f"**Your response:** {form_data['post_launch_priority']}")