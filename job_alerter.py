import os
import smtplib
import json
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# --- Configuration ---
# Your email credentials (use environment variables for security in production)
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'ksnkrishna98@gmail.com')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', 'bcvdqnvaeimgaios') # This has been updated with your provided App Password
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL', 'ksnkrishna98@gmail.com')

# Job search criteria
KEYWORDS = [
    'Power BI Developer',
    'SQL Developer',
    'Snowflake Developer',
    'BI Engineer',
    'Business Analyst',
    'Data Analyst' # Added Data Analyst
]
LOCATIONS = [
    'Bangalore',
    'Remote',
    'Bengaluru', # Common alternative spelling
    'Work From Home', # Common alternative for remote
    'Hyderabad', # Added Hyderabad
    'Pune' # Added Pune
]
EXPERIENCE_RANGE = (3, 5)  # Min and Max years of experience (inclusive)

# File to log sent jobs (will be created if it doesn't exist)
LOG_FILE = 'sent_jobs.json'

# --- Helper Functions ---

def load_sent_jobs():
    """Loads previously sent job IDs from the log file."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                print(f"Warning: {LOG_FILE} is corrupted or empty. Starting with an empty log.")
                return set()
    return set()

def save_sent_jobs(job_ids):
    """Saves current job IDs to the log file."""
    with open(LOG_FILE, 'w') as f:
        json.dump(list(job_ids), f)

def send_email(subject, body, receiver_email):
    """Sends an email using Gmail SMTP."""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html')) # Use 'html' for rich text

        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print(f"Email sent successfully to {receiver_email}!")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def simulate_fetch_jobs():
    """
    Simulates fetching new job postings.
    In a real application, this would involve web scraping or API calls
    to Naukri, LinkedIn, Foundit, etc.

    Returns a list of dictionaries, each representing a job.
    Each job should have: 'id', 'title', 'company', 'description', 'skills', 'link'.
    """
    print("Simulating job fetching...")
    # Example job data - replace with actual scraping logic
    jobs = [
        {
            'id': 'job1001',
            'title': 'Senior Data Analyst',
            'company': 'Tech Solutions Inc.',
            'description': 'Looking for a data analyst with strong Power BI and SQL skills. Experience with Snowflake is a plus. 4-6 years experience required.',
            'skills': ['Power BI', 'SQL', 'Data Analysis', 'Snowflake'],
            'link': 'https://example.com/job1001',
            'location': 'Bangalore',
            'experience': '4-6 Years'
        },
        {
            'id': 'job1002',
            'title': 'Junior Python Developer',
            'company': 'CodeCrafters',
            'description': 'Entry-level Python role. No specific experience required.',
            'skills': ['Python', 'Django'],
            'link': 'https://example.com/job1002',
            'location': 'Remote',
            'experience': '0-2 Years'
        },
        {
            'id': 'job1003',
            'title': 'Snowflake Developer',
            'company': 'DataWorks Co.',
            'description': 'Seeking a Snowflake Developer with 3-5 years of experience. Knowledge of data warehousing concepts is essential.',
            'skills': ['Snowflake', 'Data Warehousing', 'SQL'],
            'link': 'https://example.com/job1003',
            'location': 'Hyderabad', # This job will now match location
            'experience': '3-5 Years'
        },
        {
            'id': 'job1004',
            'title': 'Power BI Specialist',
            'company': 'Analytics Hub',
            'description': 'Expert in Power BI dashboards and reporting. 5+ years experience. Remote position.',
            'skills': ['Power BI', 'DAX', 'Reporting'],
            'link': 'https://example.com/job1004',
            'location': 'Remote',
            'experience': '5+ Years'
        },
        {
            'id': 'job1005',
            'title': 'Data Analyst - Remote',
            'company': 'Global Insights',
            'description': 'Seeking a Data Analyst with 3 years of experience. Strong analytical skills. Familiarity with Power BI is a plus.',
            'skills': ['Data Analysis', 'Excel', 'Power BI'],
            'link': 'https://example.com/job1005',
            'location': 'Remote',
            'experience': '3 Years'
        },
        {
            'id': 'job1006', # This job will be new and should be sent
            'title': 'Lead Snowflake Engineer',
            'company': 'Cloud Data Solutions',
            'description': 'Looking for a lead Snowflake engineer with 6-8 years of experience. Must have strong leadership skills.',
            'skills': ['Snowflake', 'Cloud', 'Leadership'],
            'link': 'https://example.com/job1006',
            'location': 'Bangalore',
            'experience': '6-8 Years' # Outside our experience range
        },
        {
            'id': 'job1007',
            'title': 'Data Engineer',
            'company': 'Pune Tech',
            'description': 'Seeking a Data Engineer with 4 years of experience. Python and SQL skills required.',
            'skills': ['Python', 'SQL', 'ETL'],
            'link': 'https://example.com/job1007',
            'location': 'Pune', # This job will now match location
            'experience': '4 Years'
        },
        {
            'id': 'job1008',
            'title': 'BI Engineer',
            'company': 'Analytics Co.',
            'description': 'BI Engineer with 3-5 years experience. Strong in Power BI and data warehousing.',
            'skills': ['Power BI', 'Data Warehousing', 'SQL'],
            'link': 'https://example.com/job1008',
            'location': 'Hyderabad',
            'experience': '3-5 Years'
        },
        {
            'id': 'job1009',
            'title': 'Business Analyst',
            'company': 'Consulting Inc.',
            'description': 'Business Analyst with 4 years experience. Requirements gathering and stakeholder management.',
            'skills': ['Business Analysis', 'Requirements Gathering'],
            'link': 'https://example.com/job1009',
            'location': 'Bangalore',
            'experience': '4 Years'
        }
    ]
    # Add a job that was already sent to test duplicate logic
    # In a real scenario, this would come from the fetched data
    # For simulation, we'll manually add an ID that will be in our 'sent_jobs.json'
    # For the first run, assume job1001 was already sent
    # For subsequent runs, new jobs will be added to the log
    return jobs

def parse_experience(experience_str):
    """
    Parses experience string (e.g., '3-5 Years', '5+ Years', 'Entry Level')
    into a (min_exp, max_exp) tuple.
    Returns (0, 0) for entry level, (min_val, float('inf')) for 'X+ Years'.
    """
    experience_str = experience_str.lower().replace('years', '').strip()
    if 'entry' in experience_str or 'fresher' in experience_str or '0' in experience_str:
        return (0, 0)
    if '+' in experience_str:
        min_val = int(experience_str.split('+')[0].strip())
        return (min_val, float('inf'))
    if '-' in experience_str:
        parts = experience_str.split('-')
        if len(parts) == 2:
            try:
                min_val = int(parts[0].strip())
                max_val = int(parts[1].strip())
                return (min_val, max_val)
            except ValueError:
                return (0, float('inf')) # Fallback if parsing fails
    try:
        single_val = int(experience_str.strip())
        return (single_val, single_val)
    except ValueError:
        return (0, float('inf')) # Default to broad range if parsing is difficult

def filter_job(job):
    """
    Filters a single job based on defined criteria.
    Returns True if the job matches, False otherwise.
    """
    title = job.get('title', '').lower()
    description = job.get('description', '').lower()
    skills = [s.lower() for s in job.get('skills', [])]
    location = job.get('location', '').lower()
    experience_str = job.get('experience', '0-0 Years')

    # Keyword check (title, description, or skills)
    keyword_match = any(
        any(kw.lower() in text for text in [title, description] + skills)
        for kw in KEYWORDS
    )
    if not keyword_match:
        return False

    # Location check
    location_match = any(loc.lower() in location for loc in LOCATIONS)
    if not location_match:
        return False

    # Experience check
    job_min_exp, job_max_exp = parse_experience(experience_str)
    required_min_exp, required_max_exp = EXPERIENCE_RANGE

    # Check for overlap in experience ranges
    # A match occurs if the job's min_exp is within or below the required max_exp,
    # AND the job's max_exp is within or above the required min_exp.
    experience_match = (
        job_min_exp <= required_max_exp and
        (job_max_exp >= required_min_exp or job_max_exp == float('inf'))
    )
    if not experience_match:
        return False

    return True

def generate_email_body(job):
    """Generates the HTML body for the job alert email."""
    return f"""
    <html>
    <head></head>
    <body>
        <p>Hello,</p>
        <p>A new job matching your criteria has been found!</p>
        <h3>{job.get('title', 'N/A')}</h3>
        <p><strong>Company:</strong> {job.get('company', 'N/A')}</p>
        <p><strong>Location:</strong> {job.get('location', 'N/A')}</p>
        <p><strong>Experience:</strong> {job.get('experience', 'N/A')}</p>
        <p><strong>Key Skills:</strong> {', '.join(job.get('skills', ['N/A']))}</p>
        <p><strong>Description:</strong> {job.get('description', 'N/A')[:200]}...</p>
        <p><a href="{job.get('link', '#')}">Direct Apply Link</a></p>
        <p>Best regards,<br>Your Job Alert System</p>
    </body>
    </html>
    """

def main():
    """Main function to run the job alert system."""
    print(f"[{datetime.now()}] Starting job alert system...")
    sent_jobs = load_sent_jobs()
    print(f"Loaded {len(sent_jobs)} previously sent jobs.")

    try:
        new_jobs = simulate_fetch_jobs() # Replace with actual scraping/API calls
        found_new_matches = 0

        for job in new_jobs:
            job_id = job.get('id')
            if not job_id:
                print(f"Skipping job with no ID: {job.get('title', 'Unknown Title')}")
                continue

            if job_id in sent_jobs:
                print(f"Job '{job.get('title', 'N/A')}' (ID: {job_id}) already sent. Skipping.")
                continue

            if filter_job(job):
                print(f"Found new matching job: {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")
                subject = f"New Job Alert: {job.get('title', 'N/A')} at {job.get('company', 'N/A')}"
                body = generate_email_body(job)

                # Retry logic for sending email
                retries = 3
                for i in range(retries):
                    if send_email(subject, body, RECEIVER_EMAIL):
                        sent_jobs.add(job_id)
                        found_new_matches += 1
                        break
                    else:
                        print(f"Email sending failed for {job_id}. Retrying ({i+1}/{retries})...")
                        time.sleep(5) # Wait before retrying
                else:
                    print(f"Failed to send email for job {job_id} after {retries} retries.")
            else:
                print(f"Job '{job.get('title', 'N/A')}' (ID: {job_id}) did not match criteria.")

        if found_new_matches == 0:
            print("No new matching jobs found this run.")
        else:
            print(f"Sent alerts for {found_new_matches} new jobs.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        save_sent_jobs(sent_jobs)
        print(f"[{datetime.now()}] Job alert system finished. Total sent jobs logged: {len(sent_jobs)}")

if __name__ == "__main__":
    main()
