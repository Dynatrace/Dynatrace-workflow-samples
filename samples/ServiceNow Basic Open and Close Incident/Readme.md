Workflow (WF) to demonstrate basic logic for opening and closing ServiceNow incidents:
- WF will be triggered on problem open and close. 
- Task A: Search if SNOW incident already exists in SNOW
- Task B: If SNOW incident does not exist AND new Problem (event.status = OPEN) ---> create new incident in SNOW
- Task C: If SNOW incident does exist AND Problem was closed in DT (event.status = CLOSED) ---> resolve incident in SNOW

The focus of this WF sample is to demonstrate the opening and closing logic for ServiceNow incidents with conditional Jinja expressions:
- If new DT problem opens  ---> create SNOW incident
- If new DT problem closes ---> resolve SNOW incident

All other aspects of the WF are intentionally kept basic (using WF ServiceNow task defaults), to help you get started as quickly as possible after importing this WF. This WF sample can then be expanded further based on your requirements.

