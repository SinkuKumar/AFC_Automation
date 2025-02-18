# AFC Automation - Development Guidelines

**Note:**

This document serves as a collection of best practices, past experiences, and modularization approaches, intended to guide developers in the creation of automation scripts. While this document offers a structured methodology for script development, it’s important to note that it is not guaranteed to be 100% accurate or to represent the absolute best approach for every situation.

The contents of this document are based on my personal best practices, the specific requirements provided by GraphX, and my experience with automation. While I believe the suggested approach is the most effective, it may not always be the perfect solution for every scenario. Developers are encouraged to consider the context and requirements of their specific project when applying these practices.

## Introduction

The **AFC Urgent Care automation** is built on the **Experity portal** and requires browser-based automation. In the past, we have used **Selenium**, and we will continue to leverage this tool for automation moving forward. 

In addition to browser automation, several important considerations are required in this process:
- **File-based logging** for tracking script execution.
- **Email and WhatsApp notifications** for alerting users upon script completion.
- A **table-based log in the database** for historical analysis and easy access to past data.

To improve simplicity and user experience, we will provide clear console messages that indicate the status of manual data uploads, ensuring users are informed of the script's progress. 

**Error codes** will also be introduced to offer more precise feedback about the script’s status and any encountered issues, making it easier to identify and resolve problems.

It is essential that the script development follows **PEP-8** specifications for Python code styling. The guidelines can be found here: [PEP-8 Guide](https://peps.python.org/pep-0008/).

The script must be developed in accordance with these guidelines to ensure consistency, maintainability, and readability.

### **Core Modules and Environment Protection**

To maintain the integrity of the production environment, the **core modules** will be set to **read-only**. This ensures that no unintended or direct modifications can be made in production. Any necessary changes to the core modules will be implemented via a **custom CI/CD pipeline**, which will enforce a controlled, versioned process for deploying changes. All changes must be made locally first and then pushed through the pipeline for testing, review, and deployment. This approach guarantees that production systems remain stable and secure while enabling efficient development and updates.

