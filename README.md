# PHC Clubs Information Collector

A Streamlit application for collecting information about clubs and sending it via email.

## Features

- Form-based collection of club information
- Support for multiple presidents and vice-presidents
- Email functionality to send collected information
- Clean and user-friendly interface

## Setup Instructions

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/phclubs_info_collector.git
   cd phclubs_info_collector
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Rename `sample.env` to `.env` and update with your email credentials:
   ```
   # Email Configuration
   EMAIL_USER=your_email@2925.com
   EMAIL_PASSWORD=your_email_password
   RECIPIENT_EMAIL=recipient@example.com
   ```
   Replace the values with your actual email credentials.

## Running the Application

Run the Streamlit app with:

```
streamlit run main.py
```

The application will be available at http://localhost:8501 in your web browser.

## Email Configuration

This application uses SMTP to send emails with the following settings:
- SMTP Server: smtp.2925.com
- SMTP Port: 25 (plain)

You can also use these settings for other protocols:
- IMAP: imap.2925.com:143 (plain)
- POP3: pop3.2925.com:110 (plain)

## Usage

1. Fill in the club information form
2. Upload a background picture (optional)
3. Click "Submit" to send the information via email
4. If email credentials are not set, a preview of the email content will be shown 