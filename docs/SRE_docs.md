# CI/CD Pipeline SRE Documentation

This document outlines the Service Level Indicators (SLIs), Service Level Objectives (SLOs), and other key SRE practices for our CI/CD pipeline.

## Service Level Indicators (SLIs)

### Availability

* **Definition:** The proportion of time our CI/CD pipeline is available and functioning as expected.
* **Metric:** `successful_runs / total_runs`
* **Implementation:** We track the number of successful pipeline runs and the total number of runs using Google Cloud Monitoring. A successful run is defined as a pipeline execution where all stages complete without errors. Availability is calculated over a rolling 24-hour window.
* **Monitoring:** We monitor availability across all stages of our pipeline, including build, test, and deploy.  Dashboards are available in Google Cloud Monitoring  **link coming soon*.

### Latency

* **Definition:** The time it takes for a CI/CD pipeline run to complete.
* **Metric:** `average_pipeline_duration`
* **Implementation:** We measure the duration of each pipeline run and calculate the average duration over a 1-hour rolling window using Google Cloud Monitoring.
* **Monitoring:** We track latency for different types of pipeline runs, such as full builds and deployments triggered by code pushes to the `main` branch. Latency metrics are visualized in  **link coming soon*.

### Error Rate

* **Definition:** The proportion of CI/CD pipeline runs that fail.
* **Metric:** `failed_runs / total_runs`
* **Implementation:** We track the number of failed pipeline runs and the total number of runs using Google Cloud Monitoring. A failed run is defined as a pipeline execution where any stage encounters an error.
* **Monitoring:** We categorize different types of errors, such as build errors, test failures, and deployment errors. Error rate trends are available in **link coming soon*.


## Service Level Objectives (SLOs)

### Availability SLO

* **Objective:** 99.9% of CI/CD pipeline runs should be successful.
* **SLI:** Availability
* **Error Budget:** We have an error budget of 0.1% of downtime per month for our CI/CD pipeline. This allows for some controlled disruption for maintenance or deployments of new features.
* **Alerting:** Alerts are triggered if availability drops below 99.9%, notifying the on-call engineer via PagerDuty.
* **Tracking:** We track our availability error budget using a burn-down chart in Google Cloud Monitoring **link coming soon*. If we are in danger of exceeding our error budget, we will temporarily halt feature deployments and prioritize reliability fixes.

### Latency SLO

* **Objective:** 95% of CI/CD pipeline runs should complete within 10 minutes.
* **SLI:** Latency
* **Alerting:** Alerts are triggered if more than 5% of pipeline runs exceed the 10-minute threshold, notifying the on-call engineer via PagerDuty.
* **Tracking:** We track latency SLO breaches using alerts and dashboards in Google Cloud Monitoring. If we consistently exceed our latency error budget, we will investigate performance bottlenecks and optimize resource allocation (e.g., increase build machine resources, optimize Docker image sizes).

### Error Rate SLO

* **Objective:** Less than 1% of CI/CD pipeline runs should fail.
* **SLI:** Error Rate
* **Alerting:** Alerts are triggered if the error rate exceeds 1%, escalating to the on-call engineer via PagerDuty.
* **Tracking:** We monitor error rate using Google Cloud Monitoring and categorize errors by severity. If our error rate approaches the budget limit, we will conduct root cause analysis on frequent errors and implement preventative measures.


## Error Budgets

* **Availability Error Budget Target:** Maintain an error budget of 0.1% downtime per month.
* **Latency Error Budget Target:** Ensure that no more than 5% of pipeline runs exceed the 10-minute latency threshold.
* **Error Rate Budget Target:** Maintain an error rate of less than 1% of CI/CD pipeline runs.


## Toil

* **Manual Interventions Target:** Reduce manual interventions to less than 5% of all CI/CD pipeline runs.
* **Automated Tasks Target:** Automate at least 90% of all CI/CD pipeline tasks.
* **Time Spent on Toil Target:** Reduce the time spent on manual operational tasks to less than 10 hours per month.

**Toil Reduction Strategies:**

* **Manual Interventions:** 
    * Examples of manual interventions we aim to reduce include manually restarting failed builds, manually approving deployments, and manually cleaning up build artifacts.
    * We will reduce these interventions by implementing automatic retries for transient errors, automating deployment approvals for low-risk changes, and configuring automatic cleanup of build artifacts.
* **Automated Tasks:** 
    * We will automate tasks such as infrastructure provisioning, test environment setup, deployment rollbacks, and pipeline configuration management.
    * We will use tools such as Terraform, Ansible, and Kubernetes to achieve automation.
* **Time Spent on Toil:**
    * We will track time spent on manual tasks using time tracking software integrated with our project management system.
    * We will regularly review this data to identify opportunities for further automation and process improvements.


## Playbooks/Runbooks

### Pipeline Failure Due to Dependency Issue

* **Symptoms:** Builds fail with error messages indicating missing or inaccessible dependencies (e.g., "Could not resolve dependency," "Connection timed out").
* **Troubleshooting Steps:**
    1. Check the dependency repository (e.g., PyPI for Python packages) for outages or known issues.
    2. Verify network connectivity to the dependency repository from the build environment.
    3. Inspect the `requirements.txt` or `setup.py` file to ensure dependency versions are correct and that there are no conflicts.
    4. Check the local dependency cache (e.g., `.cache/pip` directory) for corrupted files.
    5. If using a private dependency repository, check its availability and authentication configuration.
* **Escalation:** If the issue cannot be resolved within 30 minutes, escalate to lara-sundare6.

### Pipeline Failure Due to Test Failures

* **Symptoms:** The pipeline fails during the testing stage with error messages indicating failing tests.
* **Troubleshooting Steps:**
    1. Examine the test failure reports to identify the specific failing tests and the reasons for failure.
    2. Run the failing tests locally in the development environment to reproduce the issue.
    3. Debug the code to identify and fix the root cause of the test failures.
    4. If the failures are due to flaky tests, investigate the test environment or test data for inconsistencies.
* **Escalation:** If the issue cannot be resolved within 1 hour and is blocking releases, escalate to lara-sundare6.* **Escalation:** If the issue cannot be resolved within 1 hour and is blocking releases, escalate to lara-sundare6.

## On-Call and Escalation Procedures

* **On-Call Rotation:** lara-sundare6 follows a weekly on-call rotation. The on-call engineer is responsible for responding to CI/CD pipeline incidents and alerts.
* **Escalation Paths:**
    * **Severity 1 (Critical):** Pipeline is completely down, blocking all deployments. Escalate to the SRE, 'lara-sundare6' immediately.
    * **Severity 2 (Major):** Pipeline is experiencing significant delays or errors, impacting releases. Escalate to lara-sundare6 within 1 hour.
    * **Severity 3 (Minor):** Intermittent issues or minor errors that do not significantly impact deployments. The on-call engineer handles these issues.
* **Communication Channels:**
    * PagerDuty for alerts and escalations.
    * Dedicated Slack channel (`#ci-cd-alerts`) for incident communication and updates.
    * Google Meet for conference calls if necessary.

This documentation is a living document and will be updated as our CI/CD pipeline evolves and we gain more operational experience.
