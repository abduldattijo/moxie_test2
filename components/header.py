import streamlit as st

def display_header():
    """Display Roy's logo, header and subtitle"""
    # Roy's image placeholder
    roy_image_html = """
    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <div style="width: 150px; height: 150px; background-color: #2C3E50; border-radius: 50%; 
                display: flex; justify-content: center; align-items: center; color: white; font-weight: bold; font-size: 24px;">
            Roy
        </div>
    </div>
    """
    st.markdown(roy_image_html, unsafe_allow_html=True)
    
    # Header and subtitle
    st.markdown('<div class="main-header">Launch Smarter with Roy</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">I\'ve studied the strategies behind thousands of launches. Let\'s create one that gets your startup seen, trusted, and funded.</div>', unsafe_allow_html=True)

def display_footer():
    """Display footer with credit"""
    st.markdown("<div style='text-align: right; color: #888; font-size: 0.8rem; margin-top: 20px;'>Stephanie LaFlora</div>", unsafe_allow_html=True)