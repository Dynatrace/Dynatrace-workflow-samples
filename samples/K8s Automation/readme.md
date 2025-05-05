# K8s Automation Samples and onboarding 


**1. Use Operator-based rollout to configure K8s Automation**

Follow the instructions at https://docs.dynatrace.com/docs/ingest-from/setup-on-k8s/guides/deployment-and-configuration/edgeconnect/kubernetes-automation and https://docs.dynatrace.com/docs/ingest-from/setup-on-k8s/guides/deployment-and-configuration/edgeconnect/kubernetes-automation/edge-connect-kubernetes-automation-operator-supported-setup to:
- Create an oAuth client and store it in [secret.yaml](/secret.yaml)
- Configure roles for the desired automation use cases in [role.yaml](/role.yaml)
- Create a service account with [serviceaccount.yaml](/serviceaccount.yaml), which will be impersonated to trigger the Kubernetes API Server
- Link the service account with configured roles in [rolebinding.yaml](/rolebinding.yaml)
- Configure K8s Automation with Operator to deploy EdgeConnect in the Dynatrace namespace, configure EdgeConnect and the K8s connection in Dynatrace with [edgeconnect.yaml](/edgeconnect.yaml)

Apply each file with kubectl apply -f xxxx.yaml 

**2. Optional: For a simulation and test setup you can create a pod, which will stay in termination state**

Create a pod, which will be stuck in the terminating phase, once you delete it with [podtermination.yaml](/podtermination.yaml)
If required for security reasons, replace the image with a trusted image on your side. 

**4. Workflow**

Head to workflows and select upload [wftpl_k8s_pod_cleanup_simple.yaml](/wftpl_k8s_pod_cleanup_simple.yaml)
Selete the connection that you specified in [edgeconnect.yaml](/edgeconnect.yaml). 
Activate the workflow trigger.

**5. Simulate the problem**

Delete the pod "pod-stuck" with kubectl delete pods pod-stuck

**4. Kubernetes App and Anomaly Detection**

Ensure that you have configured the Detection of pods stuck in the pending and terminating phase in Settings/Anomaly Detection/Workloads. For details see https://docs.dynatrace.com/docs/observe/infrastructure-monitoring/container-platform-monitoring/kubernetes-app/reference/anomaly-detectors
Open the Kubernetes app, select "Pods" and filter for a (test) cluster in your environment. You'll see an overview of your pods, state, namespace and more. 

**5. Monitor the workflow**

After the configured timeframe (Default 10min), the workflow will kick in and forcefully delete the pod. 



  
