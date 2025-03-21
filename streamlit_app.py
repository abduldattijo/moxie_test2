import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

# Set page config
st.set_page_config(
    page_title="Moxie | High-Impact Launch Assistant",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Moxie branding
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

# Load recommendations data
@st.cache_data
def load_recommendations():
    # This would ideally be loaded from a database or CSV
    # For now, we'll hardcode some examples based on the decision tree document
    recommendations = {
        "launch_strategies": {
            "new_product": {
                "bootstrapped": {
                    "get_users": [
                        "Beta testing + early adopters program",
                        "Earned PR through founder story",
                        "High-impact partnerships with complementary products"
                    ],
                    "attract_investors": [
                        "Showcasing early user testimonials and traction",
                        "Targeted outreach to angel investors",
                        "Strategic industry events participation"
                    ]
                },
                "under_1m": {
                    "get_users": [
                        "Laser-focused ad campaigns on highest-converting channels",
                        "Content marketing highlighting problem solving",
                        "Referral program with compelling incentives"
                    ]
                }
                # Add more combinations as needed
            },
            "rebrand": {
                "series_a": {
                    "build_press": [
                        "Big media push with embargoed announcements",
                        "Paid influencer collaborations",
                        "High-end content storytelling across channels"
                    ]
                }
            }
        },
        "next_steps": {
            "bootstrapped": [
                "Focus on founder-led storytelling through podcasts and guest posts",
                "Design a customer acquisition funnel with clear conversion points",
                "Build a weekly content calendar that reinforces your unique value prop"
            ],
            "under_1m": [
                "Run small test campaigns across 3 channels to identify highest ROI",
                "Create investor-ready metrics dashboard showing key growth indicators",
                "Develop case studies from your first 10 customers"
            ],
            "1m_3m": [
                "Implement PR outreach strategy targeting tier 1 and industry publications",
                "Build scalable growth experiments with clear success metrics",
                "Create quarterly investor updates highlighting traction milestones"
            ],
            "3m_plus": [
                "Launch category-defining thought leadership campaign",
                "Plan high-visibility launch event",
                "Implement influencer partnership program"
            ]
        }
    }
    return recommendations

recommendations = load_recommendations()

# Helper function to generate email content
def generate_email_content(user_data, strategies, next_steps):
    email_content = f"""
Hey {user_data['first_name']},

First off—big congrats on building {user_data['startup_name']}. I know firsthand how intense launching a startup can be, and I built Moxie AI to help founders like you get the visibility you need to succeed.

Based on what you shared, here's your high-impact launch plan:

🔹 **Launch Type:** {user_data['launch_type']}
🔹 **Funding Stage:** {user_data['funding_status']}
🔹 **Your Primary Goal:** {user_data['primary_goal']}

✨ **Your Personalized Launch Plan:**
1. {strategies[0]}
2. {strategies[1]}
3. {strategies[2]}

📌 **Your Next Steps:**
1. {next_steps[0]}
2. {next_steps[1]}
3. {next_steps[2]}

💡 **Ready to execute?** You can take one of these three paths:

1️⃣ **DIY ($29/month):** Get an automated weekly launch roadmap so you stay on track.
2️⃣ **Coaching ($500/month):** Get direct guidance & accountability to keep momentum.
3️⃣ **Full-Service ($5K over 3 months):** Let us run your launch for you.

📅 If you ever want a deeper strategy session, let's chat. Otherwise, keep me posted—I'll be cheering for you.

Best,
Steph
    """
    return email_content

# Function to send email
def send_email(to_email, subject, body):
    # This is a placeholder. In production, connect to Zapier or SMTP
    st.success(f"Email would be sent to {to_email} with subject: {subject}")
    st.info("For implementation, connect this to Zapier or configure SMTP settings.")
    
    # If using SMTP directly, uncomment and configure this:
    """
    sender_email = "launch@moxie.ai"
    password = "your_password"
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    
    message.attach(MIMEText(body, "plain"))
    
    with smtplib.SMTP_SSL("smtp.your-email-provider.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, message.as_string())
    """

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
                    st.experimental_rerun()
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
                st.experimental_rerun()
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
                st.experimental_rerun()
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
                st.experimental_rerun()
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
                st.experimental_rerun()
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
                st.experimental_rerun()
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
                st.experimental_rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 8: Results & Email
    elif st.session_state.step == 8:
        # Map user selections to recommendation keys
        launch_type_key = "new_product"  # Default fallback
        if "New Startup" in st.session_state.user_data['launch_type']:
            launch_type_key = "new_product"
        elif "Rebrand" in st.session_state.user_data['launch_type']:
            launch_type_key = "rebrand"
        
        funding_key = "bootstrapped"  # Default fallback
        if "Bootstrapping" in st.session_state.user_data['funding_status']:
            funding_key = "bootstrapped"
        elif "under $1M" in st.session_state.user_data['funding_status']:
            funding_key = "under_1m"
        elif "$1M-$3M" in st.session_state.user_data['funding_status']:
            funding_key = "1m_3m"
        elif "$3M+" in st.session_state.user_data['funding_status']:
            funding_key = "3m_plus"
        
        goal_key = "get_users"  # Default fallback
        if "Get Users" in st.session_state.user_data['primary_goal']:
            goal_key = "get_users"
        elif "Attract Investors" in st.session_state.user_data['primary_goal']:
            goal_key = "attract_investors"
        elif "Build Press" in st.session_state.user_data['primary_goal']:
            goal_key = "build_press"
        
        # Try to get specific recommendations, fall back to defaults if combination doesn't exist
        try:
            strategies = recommendations["launch_strategies"][launch_type_key][funding_key][goal_key]
        except KeyError:
            # Fallback to some general recommendations
            strategies = [
                "Build a compelling founder story that highlights your unique perspective",
                "Create a waitlist or early access program to build anticipation",
                "Focus on one high-impact marketing channel rather than spreading thin"
            ]
        
        next_steps = recommendations["next_steps"][funding_key]
        
        # Generate email content
        email_content = generate_email_content(
            st.session_state.user_data,
            strategies,
            next_steps
        )
        
        st.success("🎉 Your High-Impact Launch Plan is ready!")
        
        with st.container():
            st.markdown('<div class="highlight">', unsafe_allow_html=True)
            st.subheader("Your Personalized Launch Plan")
            
            # Display summary of inputs
            st.markdown(f"**Startup:** {st.session_state.user_data['startup_name']}")
            st.markdown(f"**Launch Type:** {st.session_state.user_data['launch_type']}")
            st.markdown(f"**Funding Stage:** {st.session_state.user_data['funding_status']}")
            st.markdown(f"**Primary Goal:** {st.session_state.user_data['primary_goal']}")
            
            # Display recommendations
            st.subheader("Recommended Strategies:")
            for i, strategy in enumerate(strategies, 1):
                st.markdown(f"{i}. {strategy}")
                
            st.subheader("Next Steps:")
            for i, step in enumerate(next_steps, 1):
                st.markdown(f"{i}. {step}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.subheader("Delivery Options")
        
        # Email delivery option
        if st.button("Send to My Email"):
            send_email(
                st.session_state.user_data['email'],
                f"Your High-Impact Launch Plan 🚀",
                email_content
            )
        
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
            st.experimental_rerun()

if __name__ == "__main__":
    main()