# Fast-Deploy

Fast-Deploy is a CLI tool designed to simplify the process of deploying web applications for beginners and intermediate developers. It streamlines the deployment process by leveraging Docker and Nixpacks, managing AWS configurations, and ensuring that Docker environments are set up correctly. Fast-Deploy aims to demystify the deployment process, allowing developers to focus on building their applications.

## Features

- **AWS CLI Configuration Check:** Ensures AWS CLI is properly configured for deployment.
- **Docker Configuration Verification:** Checks if Docker is installed and running, and configures it if necessary.
- **Simplified Deployment Process:** Utilizes Nixpacks for building Docker images, making the process straightforward and efficient.
- **Port Mapping for Test Runs:** Offers an option to run built Docker images with specified port mapping for immediate testing.

## Getting Started

### Prerequisites

- Docker installed on your system.
- Nixpacks installed on your system.
- AWS CLI installed and configured.
- Python 3 and pip.

### Installation

Clone the Fast-Deploy repository to your local machine:

```bash
git clone https://github.com/yourgithubusername/fast-deploy.git
cd fast-deploy
```

## Usage

- **Initialize your project:**

  This will check your AWS CLI and Docker configurations and prompt you to set up a new project.

  ```bash
  ./mycli.py init
  ```

