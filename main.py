import smtplib
import pandas as pd
import os
import time
from email.message import EmailMessage

# ========== Step 1: Load Environment Variables ==========
your_email = "your email address"
your_password = "your app password"  # Use an App Password if you're using Gmail with 2FA

if not your_email or not your_password:
    raise ValueError("Email credentials not found. Please set EMAIL_USER and EMAIL_PASS as environment variables.")

# ========== Step 2: Load CSV and Clean Headers ==========
df = pd.read_csv('hr_contacts.csv')
df.columns = df.columns.str.strip()  # remove any accidental spaces

# ========== Step 3: Set up SMTP ==========
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(your_email, your_password)

# ========== Step 4: Loop Through Contacts and Send Emails ==========
for index, row in df.iterrows():
    try:
        msg = EmailMessage()
        msg['Subject'] = f"Application for Software Developer Role at {row['Company']}"
        msg['From'] = your_email
        msg['To'] = row['Email']

        # Email Body
        body = f"""Dear {row['Name']},

I hope you're doing well. I am reaching out to express my interest in exploring suitable roles at {row['Company']}.
I am a passionate software developer with experience in Python, Django, and building real-world applications.

Please find my resume attached for your reference.

Looking forward to hearing from you.

Warm regards,  
Nauman Shaikh  
Contact: +91-XXXXXXXXXX  
LinkedIn: https://linkedin.com/in/yourprofile  
"""
        msg.set_content(body)

        # Resume Attachment
        with open("Nauman-IT-Experience.pdf", "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename="Nauman-Resume.pdf"
            )

        # Send Email
        server.send_message(msg)
        print(f"✅ Sent to {row['Email']}")
        time.sleep(2)  # avoid being flagged for spam

    except Exception as e:
        print(f"❌ Failed to send to {row.get('Email', 'Unknown')}: {e}")

# ========== Step 5: Close the Server ==========
server.quit()
