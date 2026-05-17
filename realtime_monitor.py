import time

from gmail_scanner import scan_inbox
from detector import analyze_email


def start_monitor(email_user, email_pass, email_logs):

    print("\n[PhishShield] Real-Time Monitoring Started...\n")

    while True:

        try:

            emails = scan_inbox(
                email_user,
                email_pass
            )

            print("Fetched Emails:", len(emails))

            for email in emails:

                print("EMAIL FOUND:", email)

                result = analyze_email(
                    email["subject"],
                    email["sender"],
                    email["body"]
                )

                email_data = {

                    "sender": email["sender"],

                    "subject": email["subject"],

                    "body": email["body"][:200],

                    "risk_score": result["risk_score"],

                    "status": result["status"]

                }

                email_logs.append(email_data)

                print("ADDED TO DASHBOARD")

            time.sleep(10)

        except Exception as e:

            print("[Monitor Error]", e)

            time.sleep(5)