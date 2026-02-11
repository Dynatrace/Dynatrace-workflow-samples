# Security use case workflow

This is implementation of automated Azure security response actions for handling security incidents detected through
Azure Sentinel.
When an external intrusion or suspicious activity is detected on a VM, the workflow performs the following automated
steps:

- Retrieves details of the affected VM.
- Blocks all inbound and outbound network traffic by creating and attaching an isolation Network Security Group (NSG).
- Provisions a secure investigation environment with dedicated networking components.
- Creates snapshots of the VM’s disks and deploys a cloned investigation VM from those snapshots.
- This ensures that the compromised VM is immediately isolated from the network, while its state and data are preserved
  for forensic analysis without risk of tampering.

These actions follow established Azure response procedures and enable security teams to rapidly respond to compromised
VMs by preserving forensic evidence, isolating affected resources, and providing secure investigation environments.
Follow next steps:

1. Navigate to Azure Portal and search for virtual machines.
    - Select your subscription and create a resource group (for instance `demo-incident-workflow`).
    - Give a name (for instance `vulnerable-vm`).
    - Select any region (for instance East US).
    - Select any virtual machine size.
    - Configure the Virtual Machine to your liking. For example:
        - Authentication type: Password.
        - Set a username and password for VM access.
        - Change Public inbound ports to None.
    - Hit `Create a VM`.
2. Navigate to recently created VM and copy Subscription ID.
3. Upload one workflow YAML template and three sub-workflow YAML templates to the Workflows app; they will be triggered
   sequentially in response to an Azure Sentinel alert.
    - `azure-security-incident-workflow-parent.workflow-template.yaml`
    - `azure-security-investigation-incident-rg-networking.workflow-template.yaml`
    - `azure-security-investigation-isolate-vulnerable-vm.workflow-template.yaml`
    - `azure-security-investigation-snapshot-disks-and-vm.workflow-template.yaml`

   3.1. Define the right connection or create a new one following the
   setup [guide](https://docs.dynatrace.com/docs/shortlink/automation-workflows-azure-setup).
4. Verify that all sub-workflows are properly linked in the parent workflow. For instance, `isolate_vulnerable_vm`
   workflow should be linked to the `Azure Security Investigation - Isolate Vulnerable VM` subworkflow.

   4.1 Ensure you have an SSH key pair available. If you do not have one, generate it using your system’s standard
      method (e.g., ssh-keygen on macOS/Linux or PuTTYgen on Windows). Paste the public key into the public_ssh_keys widget
      of the Azure Security Investigation - Snapshot, Disks, and VM workflow, and update the JavaScript code snippet
      accordingly.
5. Press `Run` and provide the JSON below as the example event to trigger the workflow:

   ```json
   {
     "azure.subscription": "<YOUR_SUBSCRIPTION_ID>",
     "azure.resource.group": "<YOUR_RESOURCE_GROUP>",
     "azure.resource.name": "<YOUR_VM_NAME>"
   }
   ```

**Note**: After the workflow is executed, an Azure resource lock is automatically created for the affected virtual
machine.
The lock prevents deletion or modification of the VM during the security investigation, ensuring that forensic evidence
remains intact.
`SEC-INVEST-DONOTDELETE` – prevents accidental deletion.
`SEC-INVEST-DONOTMODIFY` – prevents changes to the resource.
These locks should be removed only after the investigation is complete and the resources are no longer required.

___
After successful execution, you should see a new resource group created in Azure with the given name.
In our example, a new `incident-workflow` resource group was created to serve as a dedicated space for all resources
generated during the process:

- A virtual machine for conducting the investigation.
- A snapshot of the source VM’s disks.
- A network security group with rules blocking all inbound and outbound traffic.
- A disk cloned from the source VM, which can be used for forensic analysis.

How to clean up after running the workflow:

1. At the Azure Portal, navigate to the previously created resource group at the step 1, find `Settings` → `Locks` and
   delete both
   `SEC-INVEST-DONOTDELETE` and `SEC-INVEST-DONOTMODIFY`.
2. Delete the virtual machine.
3. Delete the resource group `incident-workflow`.