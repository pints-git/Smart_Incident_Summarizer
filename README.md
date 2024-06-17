# Smart_Incident_Summarizer

## Overview

This project integrates ServiceNow and Ansible Tower to automate incident management. When a high-priority incident is created or updated in ServiceNow, a business rule triggers an Ansible Tower job. The job runs a Python script that fetches work notes, generates a summary using OpenAI, and updates the incident summary in ServiceNow.

## Prerequisites

- ServiceNow instance with appropriate access and API credentials.
- Ansible Tower instance with the necessary configuration.
- OpenAI API key.
- Python environment with `requests` and `openai` packages installed.

## Architecture

1. **ServiceNow Business Rule**: Triggers an Ansible Tower job on high-priority incidents.
2. **Ansible Tower Job**: Runs a Python script to process the incident.
3. **Python Script**: Fetches work notes from ServiceNow, generates a summary using OpenAI, and updates the incident summary.


## Running the Playbook
1. **Whenever the business rule is triggered in ServiceNow, it will make a POST request to the Ansible Tower webhook, launching the job that runs the playbook. The playbook, in turn, runs the Python script to update the incident summary.
