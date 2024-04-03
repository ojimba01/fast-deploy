#!/usr/bin/env python3
import click
import logging
import json
import os
import re
import subprocess

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("fast-deploy.log"),
                        logging.StreamHandler()
                    ])


def check_aws_configuration():
    """Check for AWS CLI configuration and prompt the user to configure if not found."""
    aws_config_file = os.path.expanduser('~/.aws/config')
    aws_credentials_file = os.path.expanduser('~/.aws/credentials')

    if not os.path.exists(aws_config_file) or not os.path.exists(aws_credentials_file):
        click.echo("AWS CLI is not configured on this system.")
        if click.confirm("Do you want to configure AWS CLI now?"):
            try:
                subprocess.run(["aws", "configure"], check=True)
            except subprocess.CalledProcessError as e:
                click.echo(
                    "Failed to run 'aws configure'. Please ensure AWS CLI is installed.")
            except FileNotFoundError:
                click.echo(
                    "AWS CLI not found. Please install AWS CLI and run 'aws configure'.")
        else:
            click.echo("AWS CLI configuration is required to deploy. Exiting.")
            exit(1)
    else:
        click.echo("AWS CLI is already configured.")


def check_docker_configuration():
    """Check for Docker configuration and verify Docker daemon is running."""
    docker_config_file = os.path.expanduser('~/.docker/config.json')

    if not os.path.exists(docker_config_file):
        click.echo("Docker is not configured on this system.")
        # Prompt for Docker installation or configuration
    else:
        click.echo(
            "Docker configuration found. Verifying Docker daemon is running...")
        try:
            subprocess.run(["docker", "version"], check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            click.echo("Docker is running and accessible.")
        except subprocess.CalledProcessError as e:
            click.echo(
                "Docker daemon is not running. Please ensure Docker is installed and running.")
            exit(1)
        except FileNotFoundError:
            click.echo("Docker is not installed. Please install Docker.")
            exit(1)


@click.group()
def cli():
    """Demo CLI for webapp deployment"""
    pass


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
def init():
    """
    Initialize a new project configuration.\n

    This command sets up the necessary configuration for deploying a web application using Fast-Deploy. It performs preliminary checks for AWS CLI and Docker configurations on your system, prompts you to configure them if not found, and creates a project-specific configuration file.\n

    The initialization process includes:\n
    - Verifying AWS CLI is configured for deployment.\n
    - Checking if Docker is installed and running for building and running containers.\n
    - Prompting for a project name, which is sanitized and used to create a unique configuration file.\n

    If a configuration file already exists in the current directory, you will be prompted to overwrite it. This ensures that your project setup remains current and aligned with your deployment environment.
    """
    check_aws_configuration()
    check_docker_configuration()
    project_name = click.prompt("Please enter your project name", type=str)

    # Sanitize project name by replacing spaces, slashes, and backslashes
    sanitized_project_name = re.sub(r'[ /\\]', '_', project_name)
    config_filename = f"{sanitized_project_name}_fd_config.json"

    # Scan the directory for any existing _config.json files
    existing_configs = [f for f in os.listdir(
        '.') if f.endswith('_fd_config.json')]

    # If any existing configuration file is found, prompt for overwrite
    if existing_configs:
        click.echo(
            f"Found existing project configuration(s): {', '.join(existing_configs)}")
        confirm = click.confirm(
            "Do you want to overwrite the existing project configuration(s)?", default=False)
        if not confirm:
            click.echo("Initialization cancelled. No changes made.")
            return
        else:
            # If user confirms, delete all existing configuration files
            for config_file in existing_configs:
                os.remove(config_file)

    config = {
        "project_name": sanitized_project_name,
        "instance_type": "t2.micro",  # Default value, can be changed by user later
    }

    # Save the new configuration to a file
    with open(config_filename, 'w') as config_file:
        json.dump(config, config_file, indent=4)

    logging.info(
        f"Project '{sanitized_project_name}' initialized with new configuration, previous configurations were overwritten.")
    click.echo(
        f"Project '{sanitized_project_name}' initialized and existing configuration(s) overwritten.")


@click.command()
@click.option('-t', '--test', is_flag=True, help="Build and then test run the Docker image with port mapping.")
def build(test):
    """
    Build a Docker image using Nixpacks.\n

    Optionally test run the built image by specifying -t or --test.\n
    This will run the Docker container with specified port mapping.\n
    """
    project_path = os.getcwd()  # Assuming we are building in the current directory
    image_name = click.prompt("Please enter your image name", type=str)

    logging.info("Building Docker image with Nixpacks...")
    click.echo("Building Docker image with Nixpacks...")

    try:
        build_with_name_result = subprocess.run(
            ["nixpacks", "build", f"--name={image_name}", project_path], capture_output=True, text=True, check=True)

        if test:
            # Assuming the port mapping needs to be prompted for or is predefined
            port_mapping = click.prompt(
                "Please enter the port mapping (format: host_port:container_port)", default="8080:8080", type=str)
            run_command = f"docker run -p {port_mapping} -it {image_name}"
            subprocess.run(run_command, check=True, shell=True)
            click.echo(f"Container running with port mapping {port_mapping}")
        else:
            modified_build_with_name_output = build_with_name_result.stdout.replace(
                "docker run -it", f"docker run -p PORT:PORT -it")
            click.echo(modified_build_with_name_output)

    except subprocess.CalledProcessError as e:
        error_message = e.stderr  # Capture the standard error output for the error message
        logging.error(f"Error during the build process: {error_message}")
        click.echo(f"Error during the build process: {error_message}")
        return


@click.command()
def deploy():
    """Deploy to AWS EC2 instance (simulation)"""
    # Attempt to find any configuration files in the current directory
    config_files = [f for f in os.listdir(
        '.') if f.endswith('_fd_config.json')]

    if not config_files:
        click.echo("No project configuration found. Please run 'init' first.")
        return

    # If there's exactly one config file, use it; otherwise, prompt the user to specify the project name
    if len(config_files) == 1:
        config_filename = config_files[0]
    else:
        project_name = click.prompt(
            "Multiple projects detected. Please enter the project name", type=str)
        sanitized_project_name = re.sub(r'[ /\\]', '_', project_name)
        config_filename = f"{sanitized_project_name}_config.json"

        if not os.path.exists(config_filename):
            click.echo(
                f"No configuration found for project '{sanitized_project_name}'. Please check the project name and try again.")
            return

    with open(config_filename, 'r') as config_file:
        config = json.load(config_file)

    # Prompt for EC2 instance type with the default from config or t2.micro if not specified
    instance_type = click.prompt("Please enter the EC2 instance type",
                                 type=str, default=config.get("instance_type", "t2.micro"))
    logging.info(
        f"Deploying to AWS EC2 instance of type {instance_type}... (simulated)")
    click.echo(
        f"Deploying to AWS EC2 instance of type {instance_type}... (simulated)")


# Add commands to the CLI group
cli.add_command(init)
cli.add_command(build)
cli.add_command(deploy)

if __name__ == '__main__':
    cli()
