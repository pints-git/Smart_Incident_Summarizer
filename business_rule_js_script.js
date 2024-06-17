(function executeRule(current, previous /*null when async*/) {
    // Only trigger for high priority incidents
    if (current.priority == 1) {
        // Define the endpoint for the Ansible Tower webhook
        var url = "https://your_ansible_tower_instance/api/v2/job_templates/your_job_template_id/launch/";

        // Set up the request
        var request = new sn_ws.RESTMessageV2();
        request.setHttpMethod("POST");
        request.setEndpoint(url);
        request.setRequestHeader("Content-Type", "application/json");
        request.setRequestHeader("Authorization", "Bearer your_ansible_tower_token");

        var requestBody = {
            "extra_vars": {
                "incident_id": current.sys_id,
                "work_notes": current.work_notes.getJournalEntry(1)  // Gets the most recent work note
            }
        };
        request.setRequestBody(JSON.stringify(requestBody));

        // Execute the request
        var response = request.execute();
        var responseBody = response.getBody();
        var httpStatus = response.getStatusCode();

        if (httpStatus != 201) {
            gs.error("Failed to trigger Ansible Tower job for incident " + current.number + ". Status: " + httpStatus);
        }
    }
})(current, previous);
