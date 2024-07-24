// copy this snippet into the first JavaScript action, name the task e.g. "trigger_synthetic"
import { syntheticOnDemandMonitorExecutionsClient } from '@dynatrace-sdk/client-classic-environment-v2';


// First action.
export default async function ({ execution_id }) {

    // here is your synthetic monitor Id to execute
    const monitorIdParam = "HTTP_CHECK-2E0B59F268D6E943";

    const config = {
        body: {
            monitors: [{monitorId: monitorIdParam }], 
        }
    }

    const executionResponse = await syntheticOnDemandMonitorExecutionsClient.execute(config);
    const executionId = executionResponse.triggered[0]?.executions[0]?.executionId;
    return executionId;
}

// Copy this snippet into a second JavaScript action 
// In the options tab activate Retry on error. The number of retries and delay should exceed your average syntehtic execution time, e.g. 4 retries with 30 seconds
// Adpapt the timeout to reflect the maximum execution time, e.g. 130 seconds
import { syntheticOnDemandMonitorExecutionsClient } from '@dynatrace-sdk/client-classic-environment-v2';
import { executionsClient } from '@dynatrace-sdk/client-automation';


export default async function ({ execution_id }) {

  const getItemsResult = await executionsClient.getTaskExecutionResult({ executionId: execution_id, id: "trigger_synthetic" });
  let executionId = getItemsResult.executionId
    
  let executionResult
  do {
    executionResult = await syntheticOnDemandMonitorExecutionsClient.getExecution(
      { executionId: executionId }
    );
  } while (executionResult.executionStage !== 'EXECUTED');

  console.log("Execution result : " + JSON.stringify(executionResult));
  return { executionResult };
}
