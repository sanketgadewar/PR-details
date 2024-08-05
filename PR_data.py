import requests
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
SMTP_SERVER = 'smtp.example.com' # Replace smtp server
SMTP_PORT = 25  # Default port for unencrypted SMTP
EMAIL_SENDER = 'your-email@gmail.com'  # Replace sender email-id
EMAIL_RECEIVER = 'your-email@gmail.com'  # Replace Receiver email-id
EMAIL_SUBJECT = 'GitHub Pull Requests Summary'

# GitHub API URL
API_URL = f'https://api.github.com/repos/freeCodeCamp/freeCodeCamp/pulls'

# Calculate the date one week ago
one_week_ago = datetime.utcnow() - timedelta(weeks=1)
one_week_ago_str = one_week_ago.strftime('%Y-%m-%d')

def fetch_pull_requests(state):
    """Fetch pull requests from GitHub API."""
    params = {
        'state': state,
        'since': one_week_ago_str
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def format_pull_requests(prs, state):
    """Format pull requests into a summary string."""
    summary = f'{state.capitalize()} Pull Requests:\n'
    for pr in prs:
        summary += f"#{pr['number']} - {pr['title']}\n"
    summary += '\n'
    return summary

def send_email(subject, body, sender, receiver):
    """Send an email with the given subject and body."""
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.send_message(msg)

def main():
    # Fetch open and closed pull requests
    open_prs = fetch_pull_requests('open')
    closed_prs = fetch_pull_requests('closed')

    # Format pull requests
    open_summary = format_pull_requests(open_prs, 'open')
    closed_summary = format_pull_requests(closed_prs, 'closed')

    # Create email body
    email_body = open_summary + closed_summary

    # Send the email
    send_email(EMAIL_SUBJECT, email_body, EMAIL_SENDER, EMAIL_RECEIVER)

if _name_ == '_main_':
    main()