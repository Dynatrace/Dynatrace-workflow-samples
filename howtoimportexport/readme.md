# Export and import workflow samples

## Import or export via API

### How to access Dynatrace platform via API 

- Refer to the [documentation](https://developer.dynatrace.com/develop/access-platform-apis-from-outside/) to access platform APIs from outside and create an OAuth2 client
- Select the following scopes: automation:workflows:read, automation:workflows:write, automation:workflows:run
- Start the Launcher in your tenant, open the "API documentation App" for an OpenAPI 3.0 specification and select definition: Automation. Here you can review the API specification or download the OpenAPI definition file

### Import workflow via API

- Use <POST> /workflows to import the workflow. You can find example http calls in [examples.txt](examples.txt) 
- Alternativately you can import the workflow [import_one_wf.json](import_one_wf.json), which allows you to import workflows via a workflow


### Export  workflow via API

- Use <GET> /workflows respectively <GET> /workflows/{id} to export one or all workflows. You can find example http calls in [examples.txt](examples.txt)
- Alternativately you can import the workflow [export_all_wf.json](export_all_wf.json), which allows you to export workflows via a workflow

## Import or export via Workflow UI 

cooming soon

## Import or export via Monaco

cooming soon

