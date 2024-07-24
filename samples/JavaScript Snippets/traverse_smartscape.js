import { executionsClient } from '@dynatrace-sdk/client-automation';
import { monitoredEntitiesClient } from '@dynatrace-sdk/client-classic-environment-v2';

// This workflow action fetches service entities with a tag referring to the value provided by the workflow trigger event.
// From that entity, calling services are retrieved and returned by the action.
export default async function ({ execution_id }) {
  // get the current execution
  const ex = await executionsClient.getExecution({ id: execution_id });
  var myServiceTag = ex.params.event['tag.service']
  
  // get entityID based on event tag
  var entity_selector = `type("SERVICE"),tag("${myServiceTag}")`
  var entities_request = {
      entitySelector: entity_selector,
      fields: "+toRelationships"
  }
  var entities = await monitoredEntitiesClient.getEntities(entities_request)
  var calledEntitiesId = entities.entities[0]['toRelationships']['calls'][0].id

  // get entityName based on entityID
  entity_selector = `entityId("${calledEntitiesId}")`
  entities_request = {
     entitySelector: entity_selector
  }
  entities = await monitoredEntitiesClient.getEntities(entities_request)
  var calledEntitiesName = entities.entities[0].displayName

  // create return value
  var entity = {
    id: calledEntitiesId,
    name: calledEntitiesName
  }
  
  return { entity };
}