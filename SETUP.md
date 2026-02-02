# Newleads Daily - Setup Guide

## Quick Start (Windows)

### Step 1: Download the Repository
1. Go to https://github.com/Deanthehandyman/Newleadsdaily
2. Click the green **Code** button
3. Click **Download ZIP**
4. Extract the ZIP file to a folder on your computer (e.g., `C:\Users\YourName\Newleadsdaily`)

### Step 2: Install Python
1. Download Python 3.9+ from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check the box "Add Python to PATH"
4. Click "Install Now"
5. Wait for installation to complete

### Step 3: Open Command Prompt
1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. Navigate to your project folder:
   ```
   cd C:\Users\YourName\Newleadsdaily
   ```

### Step 4: Create Virtual Environment
Type this in Command Prompt:
```
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` at the start of your command line.

### Step 5: Install Requirements
```
pip install -r requirements.txt
```

### Step 6: Initialize Database
```
python init_db.py
```

You should see:
```
✓ Tables created!
Creating Dean user...
✓ Dean user created!

DEFAULT LOGIN:
  Email: dean@deanshandymanservice.me
  Password: changeme

⚠️  IMPORTANT: Change your password in /settings after first login!
```

### Step 7: Start the App
```
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 8: Open in Browser
Open any web browser (Chrome, Edge, Firefox) and go to:
```
http://localhost:5000/login
```

## Login Credentials (First Time)
- **Email**: dean@deanshandymanservice.me
- **Password**: changeme

## Using on Mobile (iOS/Android)

### On the Same Network
If you want to use the app on your phone while running it on your computer:

1. Find your computer's IP address:
   - In Command Prompt (while app is running), look for a line like:
   - `Running on http://192.168.1.100:5000` (your IP will be different)

2. On your phone:
   - Connect to the same WiFi network
   - Open a browser
   - Type: `http://192.168.1.100:5000/login` (use YOUR IP)

3. You should see the login screen on your phone

### Using on Remote Network (Later)
When deployed to deanshandymanservice.me, you can access it from anywhere.

## Features

### Dashboard (`/dashboard`)
- View leads sorted by distance
- See lead details (name, phone, email, address)
- Mark leads as: Contacted, Not Interested, Won, Lost

### Settings (`/settings`)
- Change maximum search radius (km)
- Toggle which services you want to see:
  - Handyman
  - Starlink Installer
  - Smart Home Expert

### Add Lead (`/admin/add-lead`)
- Manually add new leads
- Provide latitude/longitude for location
- Tag leads with services

## Troubleshooting

### "Python not found"
- Make sure you checked "Add Python to PATH" during installation
- Restart Command Prompt after Python installation

### "ModuleNotFoundError: No module named 'flask'"
- Make sure virtual environment is activated: you should see `(venv)` at start of command line
- Run: `pip install -r requirements.txt`

### "Address already in use"
- The app is trying to start on port 5000 but it's already running
- Close other instances or use: `python app.py --port 5001`

### Can't access from phone on same network
- Make sure phone and computer are on same WiFi
- Check firewall isn't blocking port 5000
- Try: `ipconfig` in Command Prompt to find your computer's IP address

## Stopping the App
Press `Ctrl + C` in the Command Prompt window where the app is running.

## Changing Your Password
1. Log in with default credentials
2. Go to Settings
3. (Password change feature coming soon - for now, password is "changeme")
