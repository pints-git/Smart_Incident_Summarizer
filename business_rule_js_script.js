(function executeRule(current, previous /*null when async*/) {
    if (current.priority == 1) {
        var url = "https://your-fastapi-instance/your-endpoint"; // Update with  FastAPI endpoint
        var request = new sn_ws.RESTMessageV2();
        request.setHttpMethod("POST");
        request.setEndpoint(url);
        request.setRequestHeader("Content-Type", "application/json");
        var requestBody = {
            "incident_id": current.sys_id,
            "work_notes": current.work_notes.getJournalEntry(1)
        };
        request.setRequestBody(JSON.stringify(requestBody));
        var response = request.execute();
        var httpStatus = response.getStatusCode();
        if (httpStatus != 200) { // Update with expected status code
            gs.error("Failed to trigger Python script for incident " + current.number + ". Status: " + httpStatus);
        }
    }
})(current, previous);
