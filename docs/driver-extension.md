# Extending the Driver-Interface for a new platform

This chapter was planned for my bachelor thesis covering this project. Sadly it didn't fit and I prefer not to further exceed the 40 page mark...

# Extending the Driver-Interface for Kubernetes

## Introduction

Within Kubernetes, Containers are further encapsulated into so called Pods. Sadly (for now), a Pod can not be modified after deployment or better: After a Pod gets initialized with one, two (or more) containers, this structure can not be modified after. One solution for this are so called "Companion containers" which will be added to stable kubernetes in the near future (tm). Another solution is to simply provide two Pods for the testing phase wheras the first pod acts as the Subject, exposing a Service to be addressable by the second Penetration-Pod. This way we have a similar architecture to the Docker-Approach with a little more structural overhead in the design.
