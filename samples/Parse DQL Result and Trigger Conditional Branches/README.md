## 1) Workflow JavaScript Template / Sample - How to (1) Parse DQL Result (Iterate JSON Array) and then (2) trigger conditional branches (Jinja Expression)

```
wftpl_workflow_javascript_-_parse_dql.yaml ---> Workflow exported via 'Download/Workflow' option in DT
wf_workflow_javascript_-_parse_dql.json ---> Workflow exported via 'Download/Template' option in DT
```

DT Workflow template / sample that shows how to achieve the following:

1) Parse the result of a DQL query in JavaScript (iterate through result JSON array).
For quick testing: DQL query (first task) generates dummy data with DQL ‘data’ command

2) Based on the the processed result from 1), then trigger conditional branches (Jinja expressions). For example: 
- If production error count > 100 ---> branch Workflow into task A
- If production error count >= 0 and <= 100 ---> branch Workflow into task B
- If production namespace not found ---> branch Workflow into task C

![image](https://github.com/Dynatrace-Tomislav/Dynatrace-workflow-samples/assets/14933193/a06ed417-acbc-4885-9bee-795f5703f2d4)


## 2) Workflow Template / Sample - Conditional branches (based on DQL result)
```
wftpl_conditions_sample.yaml ---> Workflow exported via 'Download/Workflow' option in DT
wf_conditions_sample.json ---> Workflow exported via 'Download/Template' option in DT
```

The second template / sample is a shorter version without the JavaScript step. The DQL results are evaluated directly in the conditions of the relevant branches (see screenshot below)

![WF_conditions_sample](https://github.com/Dynatrace-Tomislav/Dynatrace-workflow-samples/assets/14933193/c663fb74-16f7-47e6-ac14-9cace9d8f66f)

**Note:** While the second version (without JavaScript) basically achieves the same result, the first longer version (with JavaScript) provides a template / sample where the JavaScript task adds additional flexibility (to add more complex custom logic / processing of the DQL result in JavaScript, if needed).
