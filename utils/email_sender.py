import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, smtp_server=None, smtp_port=None, sender_email=None, password=None):
        self.smtp_server = smtp_server  # e.g., "smtp.gmail.com"
        self.smtp_port = smtp_port      # e.g., 587 for TLS
        self.sender_email = sender_email
        self.password = password
    
    def generate_email_content(self, user_data, strategies, next_steps):
        """Generate email content based on user data and recommendations"""
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
    
    def send_email(self, to_email, subject, body):
        """Send email using SMTP"""
        # Check if SMTP credentials are configured
        if not all([self.smtp_server, self.smtp_port, self.sender_email, self.password]):
            # For development/demo, just return success without sending
            return True, "Email would be sent (SMTP not configured)"
        
        try:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = to_email
            message["Subject"] = subject
            
            message.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, to_email, message.as_string())
                
            return True, "Email sent successfully"
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"

# Alternative class for Zapier integration
class ZapierEmailSender:
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url
    
    def generate_email_content(self, user_data, strategies, next_steps):
        # Same as EmailSender.generate_email_content
        pass
    
    def send_email(self, to_email, subject, body):
        """Send email using Zapier webhook integration"""
        if not self.webhook_url:
            return True, "Email would be sent (Zapier webhook not configured)"
        
        try:
            import requests
            
            payload = {
                "to_email": to_email,
                "subject": subject,
                "body": body
            }
            
            response = requests.post(self.webhook_url, json=payload)
            if response.status_code == 200:
                return True, "Email sent successfully via Zapier"
            else:
                return False, f"Zapier webhook error: {response.text}"
        except Exception as e:
            return False, f"Failed to send email via Zapier: {str(e)}"