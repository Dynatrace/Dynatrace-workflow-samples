// copy this snippet into the first JavaScript action
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

// Copy this snippet into a second JavaScript action and set it to retry every e.g. 30 seconds.
export default async function ({ execution_id }) {

    let executionResult
    do {
        executionResult = await syntheticOnDemandMonitorExecutionsClient.getExecution(
            { executionId: executionId }
        );
    } while (executionResult.executionStage !== 'EXECUTED');

    console.log("Execution result : " + JSON.stringify(executionResult));
    return { executionResult };
}
