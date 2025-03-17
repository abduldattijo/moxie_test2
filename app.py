import streamlit as st
import pandas as pd
import json
import os
from utils.recommendation_engine import RecommendationEngine
from utils.email_sender import EmailSender

# Set page config
st.set_page_config(
    page_title="Moxie | High-Impact Launch Assistant",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load external CSS
def load_css():
    with open('static/styles.css', 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
# Fall back to inline CSS if file doesn't exist
try:
    load_css()
except FileNotFoundError:
    st.markdown("""
        <style>
        .main {
            background-color: #FFFFFF;
        }
        .stButton>button {
            background-color: #FF5733;
            color: white;
            font-weight: bold;
            border-radius: 30px;
            padding: 0.5rem 2rem;
            border: none;
        }
        .stButton>button:hover {
            background-color: #E64A2E;
        }
        h1, h2, h3 {
            color: #333333;
        }
        .highlight {
            background-color: #FFF3F0;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .step-container {
            background-color: #F9F9F9;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #FF5733;
        }
        </style>
        """, unsafe_allow_html=True)

# Initialize session state for multi-step form
if 'step' not in st.session_state:
    st.session_state.step = 1

if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'first_name': '',
        'email': '',
        'startup_name': '',
        'messaging_tested': '',
        'launch_type': '',
        'funding_status': '',
        'primary_goal': '',
        'audience_readiness': '',
        'post_launch_priority': ''
    }

# Initialize recommendation engine
recommendation_engine = RecommendationEngine()

# Initialize email sender (configure with your SMTP details for production)
email_sender = EmailSender()

# Helper function to map user selections to recommendation keys
def map_selection_to_key(selection, key_type):
    """Map UI selection text to recommendation engine keys"""
    mapping = {
        'launch_type': {
            '🚀 New Startup/Product Launch': 'new_product',
            '🔄 Brand Repositioning (Rebrand or Pivot)': 'rebrand',
            '💰 Funding Announcement': 'funding',
            '📢 Major Partnership or Publicity Push': 'partnership'
        },
        'funding_status': {
            '🚀 Bootstrapping (No external funding, self-funded)': 'bootstrapped',
            '🌱 Raised under $1M (Likely still raising, early-stage)': 'under_1m',
            '📈 Raised $1M-$3M (Have 12-18 months of runway)': '1m_3m',
            '🏆 Raised $3M+ (Series A+; established growth strategy)': '3m_plus'
        },
        'primary_goal': {
            '🚀 Get Users or Customers': 'get_users',
            '💰 Attract Investors': 'attract_investors',
            '🎙 Build Press & Awareness': 'build_press',
            '🌎 Create Industry Influence': 'create_influence'
        }
    }
    
    try:
        return mapping[key_type][selection]
    except KeyError:
        # Return a default if mapping fails
        defaults = {
            'launch_type': 'new_product',
            'funding_status': 'bootstrapped',
            'primary_goal': 'get_users'
        }
        return defaults[key_type]

# Main app logic
def main():
    # Header
    st.image("https://via.placeholder.com/200x60?text=Moxie", width=200)
    st.title("High-Impact Launch Assistant")
    st.markdown("Created for founders who refuse to be ignored. Get your personalized launch plan in 3 minutes.")
    
    # Step 1: Collect basic info
    if st.session_state.step == 1:
        with st.container():
            st.markdown('<div class="step-container">', unsafe_allow_html=True)
            st.subheader("Step 1: Let's get to know you")
            
            st.session_state.user_data['first_name'] = st.text_input("First Name", 
                                                               st.session_state.user_data['first_name'])
            st.session_state.user_data['email'] = st.text_input("Email", 
                                                          st.session_state.user_data['email'])
            st.session_state.user_data['startup_name'] = st.text_input("Startup Name", 
                                                                 st.session_state.user_data['startup_name'])
            
            if st.button("Next"):
                if not st.session_state.user_data['first_name'] or not st.session_state.user_data['email'] or not st.session_state.user_data['startup_name']:
                    st.warning("Please fill out all fields to continue.")
                else:
                    st.session_state.step = 2
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 2: Messaging Validation
    elif st.session_state.step == 2:
        with st.container():
            st.markdown('<div class="step-container">', unsafe_allow_html=True)
            st.subheader("Step 2: Messaging Validation")
            
            st.markdown("""
            <div class="highlight">
            Before we dive in, have you tested your messaging with real customers?
            </div>
            """, unsafe_allow_html=True)
            
            messaging_options = [
                "✅ Yes, I've gotten direct feedback on my messaging.",
                "🤔 Sort of... I've talked to people, but nothing structured.",
                "❌ No, I haven't tested it yet."
            ]
            
            st.session_state.user_data['messaging_tested'] = st.radio(
                "Select one:", 
                messaging_options,
                index=0 if not st.session_state.user_data['messaging_tested'] else 
                      messaging_options.index(st.session_state.user_data['messaging_tested'])
            )
            
            if st.button("Next"):
                if st.session_state.user_data['messaging_tested'] == messaging_options[0]:
                    st.success("Perfect. This means your messaging is already rooted in real insights.")
                elif st.session_state.user_data['messaging_tested'] == messaging_options[1]:
                    st.info("Let's make it structured. Your first step is to interview 7 people from your ideal audience.")
                else:
                    st.warning("That's your first move. The most efficient way to validate your messaging is by putting a draft landing page in front of your audience.")
                
                st.session_state.step = 3
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 3: Launch Type
    elif st.session_state.step == 3:
        with st.container():
            st.markdown('<div class="step-container">', unsafe_allow_html=True)
            st.subheader("Step 3: What kind of launch are you preparing for?")
            
            launch_options = [
                "🚀 New Startup/Product Launch",
                "🔄 Brand Repositioning (Rebrand or Pivot)",
                "💰 Funding Announcement",
                "📢 Major Partnership or Publicity Push"
            ]
            
            st.session_state.user_data['launch_type'] = st.radio(
                "Select one:", 
                launch_options,
                index=0 if not st.session_state.user_data['launch_type'] else 
                      launch_options.index(st.session_state.user_data['launch_type'])
            )
            
            if st.button("Next"):
                st.session_state.step = 4
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 4: Funding Status
    elif st.session_state.step == 4:
        with st.container():
            st.markdown('<div class="step-container">', unsafe_allow_html=True)
            st.subheader("Step 4: Funding Status & Budget")
            
            st.markdown("""
            <div class="highlight">
            Where are you financially right now?
            </div>
            """, unsafe_allow_html=True)
            
            funding_options = [
                "🚀 Bootstrapping (No external funding, self-funded)",
                "🌱 Raised under $1M (Likely still raising, early-stage)",
                "📈 Raised $1M-$3M (Have 12-18 months of runway)",
                "🏆 Raised $3M+ (Series A+; established growth strategy)"
            ]
            
            st.session_state.user_data['funding_status'] = st.radio(
                "Select one:", 
                funding_options,
                index=0 if not st.session_state.user_data['funding_status'] else 
                      funding_options.index(st.session_state.user_data['funding_status'])
            )
            
            if st.button("Next"):
                st.session_state.step = 5
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 5: Primary Goal
    elif st.session_state.step == 5:
        with st.container():
            st.markdown('<div class="step-container">', unsafe_allow_html=True)
            st.subheader("Step 5: Primary Launch Goal")
            
            goal_options = [
                "🚀 Get Users or Customers",
                "💰 Attract Investors",
                "🎙 Build Press & Awareness",
                "🌎 Create Industry Influence"
            ]
            
            st.session_state.user_data['primary_goal'] = st.radio(
                "What's your primary goal for this launch?", 
                goal_options,
                index=0 if not st.session_state.user_data['primary_goal'] else 
                      goal_options.index(st.session_state.user_data['primary_goal'])
            )
            
            if st.button("Next"):
                st.session_state.step = 6
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 6: Audience Readiness
    elif st.session_state.step == 6:
        with st.container():
            st.markdown('<div class="step-container">', unsafe_allow_html=True)
            st.subheader("Step 6: Audience Readiness")
            
            audience_options = [
                "✅ Yes, we have an engaged community.",
                "⚡ We have a small following but need more traction.",
                "❌ No, we're starting from scratch."
            ]
            
            st.session_state.user_data['audience_readiness'] = st.radio(
                "Do you already have an audience or email list?", 
                audience_options,
                index=0 if not st.session_state.user_data['audience_readiness'] else 
                      audience_options.index(st.session_state.user_data['audience_readiness'])
            )
            
            if st.button("Next"):
                st.session_state.step = 7
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 7: Post-Launch Priority
    elif st.session_state.step == 7:
        with st.container():
            st.markdown('<div class="step-container">', unsafe_allow_html=True)
            st.subheader("Step 7: Post-Launch Priority")
            
            priority_options = [
                "📈 Scaling & repeatable traction (growth systems)",
                "💰 Investor relations & positioning for next raise",
                "🛠 Optimizing based on customer feedback",
                "🔥 Sustaining press & industry visibility"
            ]
            
            st.session_state.user_data['post_launch_priority'] = st.radio(
                "What's your biggest priority post-launch?", 
                priority_options,
                index=0 if not st.session_state.user_data['post_launch_priority'] else 
                      priority_options.index(st.session_state.user_data['post_launch_priority'])
            )
            
            if st.button("Generate My Launch Plan"):
                st.session_state.step = 8
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 8: Results & Email
    elif st.session_state.step == 8:
        # Map user selections to recommendation keys
        launch_type_key = map_selection_to_key(st.session_state.user_data['launch_type'], 'launch_type')
        funding_key = map_selection_to_key(st.session_state.user_data['funding_status'], 'funding_status')
        goal_key = map_selection_to_key(st.session_state.user_data['primary_goal'], 'primary_goal')
        
        # Get recommendations from the engine
        strategies = recommendation_engine.get_strategies(launch_type_key, funding_key, goal_key)
        next_steps = recommendation_engine.get_next_steps(funding_key)
        
        # Generate email content
        email_content = email_sender.generate_email_content(
            st.session_state.user_data,
            strategies,
            next_steps
        )
        
        st.success("🎉 Your High-Impact Launch Plan is ready!")
        
        with st.container():
            st.markdown('<div class="highlight">', unsafe_allow_html=True)
            st.subheader("Your Personalized Launch Plan")
            
            # Display summary of inputs
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Startup:** {st.session_state.user_data['startup_name']}")
                st.markdown(f"**Launch Type:** {st.session_state.user_data['launch_type'].replace('🚀 ', '').replace('🔄 ', '').replace('💰 ', '').replace('📢 ', '')}")
            with col2:
                st.markdown(f"**Funding Stage:** {st.session_state.user_data['funding_status'].replace('🚀 ', '').replace('🌱 ', '').replace('📈 ', '').replace('🏆 ', '')}")
                st.markdown(f"**Primary Goal:** {st.session_state.user_data['primary_goal'].replace('🚀 ', '').replace('💰 ', '').replace('🎙 ', '').replace('🌎 ', '')}")
            
            # Display recommendations
            st.subheader("Recommended Strategies:")
            for i, strategy in enumerate(strategies, 1):
                st.markdown(f"{i}. {strategy}")
                
            st.subheader("Next Steps:")
            for i, step in enumerate(next_steps, 1):
                st.markdown(f"{i}. {step}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.subheader("Ready to execute?")
        
        # Service tiers
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### DIY")
            st.markdown("**$29/month**")
            st.markdown("Weekly roadmap")
        with col2:
            st.markdown("### Coaching")
            st.markdown("**$500/month**")
            st.markdown("Direct guidance")
        with col3:
            st.markdown("### Full-Service")
            st.markdown("**$5K/3 months**")
            st.markdown("We run it for you")
        
        # Email delivery option
        if st.button("Send to My Email"):
            success, message = email_sender.send_email(
                st.session_state.user_data['email'],
                f"Your High-Impact Launch Plan 🚀",
                email_content
            )
            if success:
                st.success(message)
            else:
                st.error(message)
        
        # Option to start over
        if st.button("Create Another Launch Plan"):
            # Reset session state
            st.session_state.step = 1
            st.session_state.user_data = {
                'first_name': '',
                'email': '',
                'startup_name': '',
                'messaging_tested': '',
                'launch_type': '',
                'funding_status': '',
                'primary_goal': '',
                'audience_readiness': '',
                'post_launch_priority': ''
            }
            st.rerun()

if __name__ == "__main__":
    main()