'''
1. Create a FastAPI application that exposes a webhook endpoint to receive notifications from ServiceNow.
2. When a high-priority incident is created or updated in ServiceNow, the business rule sends a POST request to the FastAPI webhook endpoint.
3. The FastAPI application receives the request and triggers a Python function to process the incident.
4. The Python function fetches work notes from ServiceNow using the ServiceNow API.
5. The function generates a summary using OpenAI's API.
6. The function updates the incident summary in ServiceNow using the ServiceNow API.
'''
from fastapi import FastAPI, Request
import requests
from openai import OpenAI

app = FastAPI()

# ServiceNow credentials
sn_instance = "your_sn_instance"
sn_username = "your_sn_username"
sn_password = "your_sn_password"

# OpenAI API key
openai_api_key = "your_openai_api_key"

# ServiceNow business rule webhook endpoint
@app.post("/sn-webhook")
async def sn_webhook(request: Request):
    # Get incident details from ServiceNow
    incident_id = request.json()["incident_id"]
    sn_url = f"https://{sn_instance}.service-now.com/api/now/table/incident/{incident_id}"
    sn_headers = {
        "Authorization": f"Basic {sn_username}:{sn_password}",
        "Content-Type": "application/json"
    }
    sn_response = requests.get(sn_url, headers=sn_headers)
    incident_data = sn_response.json()

    # Fetch work notes from ServiceNow
    work_notes_url = f"https://{sn_instance}.service-now.com/api/now/table/incident_work_note?sysparm_query=incident={incident_id}"
    work_notes_response = requests.get(work_notes_url, headers=sn_headers)
    work_notes_data = work_notes_response.json()

    # Generate summary using OpenAI
    openai = OpenAI(api_key=openai_api_key)
    summary = openai.Completion.create(
        prompt="Generate a summary of the incident",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    ).choices[0].text

    # Update incident summary in ServiceNow
    update_url = f"https://{sn_instance}.service-now.com/api/now/table/incident/{incident_id}"
    update_data = {"summary": summary}
    update_response = requests.patch(update_url, headers=sn_headers, json=update_data)

    return {"message": "Incident summary updated successfully"}
