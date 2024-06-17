import sys
import requests
from requests.auth import HTTPBasicAuth
import openai

# ServiceNow credentials and instance details
SN_INSTANCE = 'your_instance'
SN_USERNAME = 'your_username'
SN_PASSWORD = 'your_password'
OPENAI_API_KEY = 'your_openai_api_key'

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

def generate_summary(work_notes):
    prompt = f"Summarize the following work notes:\n{work_notes}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    summary = response.choices[0].text.strip()
    return summary

def update_incident_summary(incident_id, summary):
    url = f'https://{SN_INSTANCE}.service-now.com/api/now/table/incident/{incident_id}'
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {"short_description": summary}
    response = requests.patch(url, auth=HTTPBasicAuth(SN_USERNAME, SN_PASSWORD), headers=headers, json=data)
    return response.json()

def main():
    if len(sys.argv) != 3:
        print("Usage: python update_incident_summary.py <incident_id> <work_notes>")
        sys.exit(1)

    incident_id = sys.argv[1]
    work_notes = sys.argv[2]

    summary = generate_summary(work_notes)
    update_response = update_incident_summary(incident_id, summary)
    print(f"Updated Incident {incident_id} with summary: {summary}")

if __name__ == "__main__":
    main()
