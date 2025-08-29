#!/usr/bin/env python3
"""
Development helper script for Azure Functions project
"""
import argparse
import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, check=True):
    """Run a shell command and return the result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check)
    return result


def setup_environment():
    """Set up the development environment"""
    print("Setting up development environment...")
    
    # Create virtual environment if it doesn't exist
    if not Path(".venv").exists():
        print("Creating virtual environment...")
        run_command("python3 -m venv .venv")
    
    # Install dependencies
    print("Installing dependencies...")
    run_command("source .venv/bin/activate && pip install --upgrade pip")
    run_command("source .venv/bin/activate && pip install -r requirements.txt")
    
    # Copy local settings if not exists
    if not Path("local.settings.json").exists():
        print("Creating local.settings.json from template...")
        run_command("cp local.settings.json.template local.settings.json")
    
    print("Development environment setup complete!")


def run_tests():
    """Run all tests"""
    print("Running tests...")
    run_command("source .venv/bin/activate && pytest tests/ -v")


def run_lint():
    """Run linting and code quality checks"""
    print("Running linting...")
    run_command("source .venv/bin/activate && ruff check .", check=False)
    run_command("source .venv/bin/activate && ruff format --check .", check=False)
    run_command("source .venv/bin/activate && mypy . --ignore-missing-imports", check=False)


def format_code():
    """Format code with ruff"""
    print("Formatting code...")
    run_command("source .venv/bin/activate && ruff format .")


def start_functions():
    """Start Azure Functions runtime"""
    print("Starting Azure Functions...")
    print("Make sure you have Azure Functions Core Tools installed!")
    run_command("source .venv/bin/activate && func start")


def clean():
    """Clean up generated files"""
    print("Cleaning up...")
    run_command("find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true")
    run_command("find . -name '*.pyc' -delete 2>/dev/null || true")
    run_command("rm -rf .pytest_cache .mypy_cache .coverage htmlcov/ dist/ build/")
    print("Cleanup complete!")


def main():
    parser = argparse.ArgumentParser(description="Development helper for Azure Functions")
    parser.add_argument("command", choices=[
        "setup", "test", "lint", "format", "start", "clean"
    ], help="Command to run")
    
    args = parser.parse_args()
    
    if args.command == "setup":
        setup_environment()
    elif args.command == "test":
        run_tests()
    elif args.command == "lint":
        run_lint()
    elif args.command == "format":
        format_code()
    elif args.command == "start":
        start_functions()
    elif args.command == "clean":
        clean()


if __name__ == "__main__":
    main()