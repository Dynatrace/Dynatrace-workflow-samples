/**
 * Get Kubernetes Connection from dynatrace.kubernetes.connector based on k8s.cluster.uid in an Event.
 * Can be used as an input to the *Connection* property in Workflow Actions of Kubernetes Connector.
 * Notes:
 *  - requires settings:objects:read scope
 *  - Feel free to fine-tune the script based on your needs (e.g., multiple namespaces)
 */
// import of sdk modules
import { execution } from '@dynatrace-sdk/automation-utils';
import { settingsObjectsClient} from '@dynatrace-sdk/client-classic-environment-v2';

export default async function () {
  // get current execution and event
  const ex = await execution();
  const event = await ex.event();
  // extract k8s.cluster.uid
  const clusterUid = event["k8s.cluster.uid"];

  if (!clusterUid) {
    throw new Error('Event does not contain k8s.cluster.uid');
  }

  console.log(`Searching for k8s.cluster.uid=${clusterUid}`);

  // find settings objects that contain the cluster uid
  const settingsObjects = await settingsObjectsClient.getSettingsObjects({
    fields: 'objectId,summary,schemaId,value',
    schemaIds: 'app:dynatrace.kubernetes.connector:connection',
    filter: `value.uid = '${clusterUid}'`
  });

  // check if any connections were found
  if (settingsObjects.items.length == 0) {
    throw new Error(`Could not find a connection for K8s Cluster with UID ${clusterUid}`)
  }

  // more than one connection found
  if (settingsObjects.items.length > 1) {
    throw new Error(`Found ${settingsObjects.items.length} connections (more than 1). Aborting...`)
  }

  // return UID of the first connection
  return settingsObjects.items[0].objectId;
}