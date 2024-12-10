from twilio.rest import Client
from urllib.parse import urlencode
import time
import os

# Environment variables for sensitive information
account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
auth_token = os.getenv('TWILIO_AUTH_TOKEN', '')

client = Client(account_sid, auth_token)

# Call parameters
to_number = ('')
from_number = ''
message = "hello!"

url = 'https://handler.twilio.com/twiml/EHfbb90737b757304c9b3cbcb81ba73770?' + urlencode({'Message': message})

retry_count = 0
max_retries = 5

while retry_count < max_retries:
    try:
        # Initiate the call
        call = client.calls.create(
            to=to_number,
            from_=from_number,
            url=url
        )
        print(f"Call initiated with SID: {call.sid}")
        call_sid = call.sid

        # Wait for call status update
        time.sleep(25)

        # Fetch call status
        call = client.calls(call_sid).fetch()
        print(f"Call Status: {call.status}")

        if 'completed' in call.status:
            print("Call answered. Exiting loop.")
            break
        else:
            print("Retrying...")
            retry_count += 1

    except Exception as e:
        print(f"Error during API call: {e}")
        break

if retry_count == max_retries:
    print("Max retries reached. Exiting.")

print("Script completed.")
