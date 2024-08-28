# Group roles and policies to add ReadOnly permissions



Classic Dynatrace Permissions Filtered by ManagementZones (i.e. EasyTravel_Prod)

Latest Dynatrace Permissions Filtered by dt.security_context or dt.host_group.id (i.e. EasyTravel_Prod, aks-noram-prod-private)

### Environment Level Scope:

* Manage support tickets


---


### Default Policies to add:

`AppEngine - User`
`Extensions - User access`
`Hub Catalog Read`


---


### Custom Parameterized Policy be created:

 `ALLOW environment:roles:viewer 
 WHERE environment:management-zone = "${bindParam:mz-name}";`
 
 `ALLOW environment:roles:replay-sessions-with-masking 
 WHERE environment:management-zone = "${bindParam:mz-name}";`
 
`ALLOW environment:roles:view-sensitive-request-data 
WHERE environment:management-zone = "${bindParam:mz-name}";`
 
 `ALLOW environment:roles:view-security-problems 
 WHERE environment:management-zone = "${bindParam:mz-name}";`

`ALLOW storage:buckets:read;`

`ALLOW storage:entities:read 
WHERE storage:dt.security_context = "${bindParam:mz-name}";`

`ALLOW storage:events:read 
WHERE storage:dt.host_group.id IN ("${bindParam:hg-name}");`

`ALLOW storage:bizevents:read 
WHERE storage:dt.host_group.id IN ("${bindParam:hg-name}");`

`ALLOW storage:metrics:read 
WHERE storage:dt.host_group.id IN ("${bindParam:hg-name}");`

`ALLOW storage:spans:read 
WHERE storage:dt.host_group.id IN ("${bindParam:hg-name}");`

`ALLOW storage:logs:read 
WHERE storage:dt.host_group.id IN ("${bindParam:hg-name}");`


---


### Steps to use this workflow:

1. Create OAuth client
2. Store Client Secret to your tenant's credential vault (same tenant where the workflow will be run)
3. Upload the template workflow
4. Open "group_definition" action and change <REPLACE-PLACEHOLDER> with your group details
5. Open "env_var" action and change <REPLACE-PLACEHOLDER> with your account id, client id, secrect's credential vault id and other necessary fileds details
6. Run your workflow.

> Note: This workflow can generate 1 group at a time. Multiple group creation will be supported in future. No promises though.


### Useful Links:

https://docs.dynatrace.com/docs/shortlink/assign-bucket-table-permissions#grail-permissions-record

https://docs.dynatrace.com/docs/manage/identity-access-management/permission-management/manage-user-permissions-policies/advanced/iam-policy-templating