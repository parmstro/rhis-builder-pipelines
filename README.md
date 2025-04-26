# rhis-builder-pipelines

Fork it. Clone it. Configure it. Test it. Change it. Commit it. Create a PR.

***

This repository contains sample application content, some vmware operations ansible, some satellite operations ansible and a node builder role. 

It is not a very organized repository.

All the roles and tasks are solid. They just have been grouped here for a lack of a more convenient logical location.  It will be reorganized eventually. If locations change, links to the new locations will be created but this original content will remain.

The platform_node_build has been exercised thoroughly in production. See the testhosts folder for some examples of how to define systems using this role. This role now exists in the rhis-builder-aap project to both build the AAP Platform Infrastructure and to automate Satellite from AAP to create nodes on:
- Baremetal
- VMware
- HyperV
- KVM
- OpenStack
- Azure (along with Image Builder)
- AWS (along with Image Builder)
- Google (along with Image Builder)
- OpenShift Virtualization

Basically, any compute resource that Satellite supports. 
For cloud instances, please see rhis-builder-imagebuilder as well. The overall workflow for cloud instances is to:
1) use rhis-builder-imagebuilder to create an imagebuilder system on an existing compute resource or baremetal
2) configure the imagebuilder to use your desired content view on satellite
3) configure the target compute resource on your satellite
4) create your imagebuilder image for the target cloud provider or image based provisioning compute resource
5) upload the image to the target compute resource
6) register the image to the satellite compute resource
7) Build whatever you need with platform_node_build

The use case that we are working on in the RHIS project is to be able to build and test an SOE (content view, configuration, etc.) across available compute resources and ensure that they are (to every extent possible) identical. RHIS wants to allow you to provision your workload anywhere. at any time. 

