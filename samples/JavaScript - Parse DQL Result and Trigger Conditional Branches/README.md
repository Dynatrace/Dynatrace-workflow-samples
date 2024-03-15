## Workflow JavaScript Template / Sample - How to (1) Parse DQL Result (Iterate JSON Array) and then (2) trigger conditional branches (Jinja Expression)

DT Workflow template / sample that shows how to achieve the following:

1) Parse the result of a DQL query in JavaScript (iterate through result JSON array).
For quick testing: DQL query (first task) generates dummy data with DQL ‘data’ command

2) Based on the the processed result from 1), then trigger conditional branches (Jinja expressions). For example: 
- If production error count > 100 ---> branch Workflow into task A
- If production error count >= 0 and <= 100 ---> branch Workflow into task B
- If production namespace not found ---> branch Workflow into task C

![image](https://github.com/Dynatrace-Tomislav/Dynatrace-workflow-samples/assets/14933193/a06ed417-acbc-4885-9bee-795f5703f2d4)
