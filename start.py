#!/usr/bin/env python3
"""
Newleads Daily Launcher

Run this with: python start.py

This script will:
1. Create virtual environment if needed
2. Install dependencies
3. Initialize database
4. Start the Flask app
"""

import os
import sys
import subprocess
import platform

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n>>> {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} failed!")
        print(f"Details: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("  NEWLEADS DAILY - STARTING APPLICATION")
    print("="*60)
    
    # Determine Python command
    python_cmd = "python3" if platform.system() != "Windows" else "python"
    
    # Step 1: Create virtual environment if it doesn't exist
    venv_dir = "venv"
    if not os.path.exists(venv_dir):
        print(f"\n>>> Creating virtual environment...")
        if platform.system() == "Windows":
            cmd = f"{python_cmd} -m venv venv"
        else:
            cmd = f"{python_cmd} -m venv venv"
        if not run_command(cmd, "Virtual environment creation"):
            print("Failed to create virtual environment")
            return False
        print("Virtual environment created successfully!")
    else:
        print(f"Virtual environment already exists")
    
    # Step 2: Activate venv and install requirements
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate.bat && "
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate && "
        pip_cmd = "venv/bin/pip"
    
    print(f"\n>>> Installing Python packages...")
    if not run_command(f"{pip_cmd} install -q -r requirements.txt", "Package installation"):
        return False
    print("Packages installed successfully!")
    
    # Step 3: Initialize database
    print(f"\n>>> Initializing database...")
    if os.path.exists("newleadsdaily.db"):
        print("Database already exists, skipping initialization")
    else:
        if platform.system() == "Windows":
            init_cmd = f"venv\\Scripts\\python init_db.py"
        else:
            init_cmd = f"venv/bin/python init_db.py"
        if not run_command(init_cmd, "Database initialization"):
            return False
        print("Database initialized successfully!")
    
    # Step 4: Start the Flask app
    print("\n" + "="*60)
    print("  STARTING FLASK APPLICATION")
    print("="*60)
    print("\nThe app is starting on: http://localhost:5000")
    print("\nLogin with:")
    print("  Email: dean@deanshandymanservice.me")
    print("  Password: changeme")
    print("\nPress Ctrl+C to stop the app")
    print("\n" + "="*60 + "\n")
    
    if platform.system() == "Windows":
        app_cmd = "venv\\Scripts\\python app.py"
    else:
        app_cmd = "venv/bin/python app.py"
    
    subprocess.run(app_cmd, shell=True)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nApp stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
