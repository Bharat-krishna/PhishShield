import imaplib
import email as email_module

from email.header import decode_header


IMAP_SERVER = "imap.gmail.com"


# -----------------------------------
# CLEAN TEXT
# -----------------------------------
def clean_text(text):

    if text is None:
        return ""

    decoded_parts = decode_header(text)

    decoded_string = ""

    for part, encoding in decoded_parts:

        if isinstance(part, bytes):

            decoded_string += part.decode(
                encoding if encoding else "utf-8",
                errors="ignore"
            )

        else:
            decoded_string += part

    return decoded_string


# -----------------------------------
# EXTRACT EMAIL BODY
# -----------------------------------
def extract_body(message):

    body = ""

    if message.is_multipart():

        for part in message.walk():

            content_type = part.get_content_type()

            content_disposition = str(
                part.get("Content-Disposition")
            )

            if (
                content_type == "text/plain"
                and "attachment" not in content_disposition
            ):

                try:

                    body = part.get_payload(
                        decode=True
                    ).decode(errors="ignore")

                except Exception:
                    pass

    else:

        try:

            body = message.get_payload(
                decode=True
            ).decode(errors="ignore")

        except Exception:
            pass

    return body


# -----------------------------------
# SCAN INBOX
# -----------------------------------
def scan_inbox(email_user, email_pass):

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)

    print("Connecting to Gmail...")

    mail.login(email_user, email_pass)

    print("Login Successful")

    mail.select("inbox")

    status, messages = mail.search(
        None,
        "ALL"
    )

    print("Search Status:", status)

    email_ids = messages[0].split()

    print("Total Emails Found:", len(email_ids))

    email_data = []

    latest_emails = email_ids[-10:]

    for e_id in latest_emails:

        print("Fetching Email ID:", e_id)

        status, msg_data = mail.fetch(
            e_id,
            "(RFC822)"
        )

        for response_part in msg_data:

            if isinstance(response_part, tuple):

                msg = email_module.message_from_bytes(
                    response_part[1]
                )

                subject = clean_text(
                    msg.get("Subject")
                )

                sender = clean_text(
                    msg.get("From")
                )

                body = extract_body(msg)

                print("EMAIL FOUND")
                print("Subject:", subject)
                print("Sender:", sender)

                email_data.append({

                    "id": e_id.decode(),

                    "subject": subject,

                    "sender": sender,

                    "body": body

                })

    mail.logout()

    return email_data