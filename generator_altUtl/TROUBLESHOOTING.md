# File Rename Utility - Troubleshooting Guide

## Error: "Unexpected token '<', "

### Symptom
When clicking the save button after renaming a file, you get an error:
```
Error renaming file: Unexpected token '<', "
```

### Root Cause
This error occurs when the JavaScript tries to parse HTML as JSON. This typically means:
1. The Flask server is not running
2. The Flask server needs to be restarted to pick up the new `/rename-file` route
3. The route is returning an HTML error page instead of JSON

### Solution

#### Step 1: Restart the Flask Server

**Stop the current server:**
- Press `Ctrl+C` in the terminal where Flask is running

**Start the server again:**
```bash
cd c:\DATA\VS_Code_Notes\SynaptixPhase2\custom_ui
python app.py
```

Or if you're using a different command:
```bash
python -m flask run
```

#### Step 2: Verify the Server is Running

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

#### Step 3: Check the Route is Registered

Open your browser and navigate to:
```
http://localhost:5000/
```

The UI should load. Check the browser console (F12) for any errors.

#### Step 4: Test the API Endpoint

Open a new terminal and test the endpoint directly:

```bash
curl -X POST http://localhost:5000/rename-file ^
  -H "Content-Type: application/json" ^
  -d "{\"folder_name\":\"TestComponent_01\",\"existing_file_name\":\"TestFile_01\",\"new_file_name\":\"TestFile_Updated\"}"
```

**Expected response:**
```json
{
  "success": false,
  "message": "Folder 'TestComponent_01' not found in project"
}
```
(This is expected if the folder doesn't exist yet)

**If you get HTML instead**, the route is not registered. Check:
1. Did you save `app.py`?
2. Did you restart the Flask server?
3. Are there any syntax errors in `app.py`?

#### Step 5: Check Import Errors

If the server fails to start, check for import errors:

```python
# In app.py, verify this line exists:
from generator_altUtl.file_rename_util import rename_file_in_folder
```

If you get an import error, verify:
1. `file_rename_util.py` exists in `generator_altUtl/` folder
2. `__init__.py` exports the function
3. No syntax errors in `file_rename_util.py`

#### Step 6: Check Browser Console

1. Open browser DevTools (F12)
2. Go to Console tab
3. Try renaming a file again
4. Look for the actual error message

The console will show:
- The request being sent
- The response received
- Any JavaScript errors

### Common Issues

#### Issue 1: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'generator_altUtl.file_rename_util'
```

**Solution:**
1. Verify `file_rename_util.py` exists
2. Check `__init__.py` has the import
3. Restart Flask server

#### Issue 2: 404 Not Found
```
404 Not Found: /rename-file
```

**Solution:**
1. Verify the route is defined in `app.py`
2. Restart Flask server
3. Check for typos in the route path

#### Issue 3: 500 Internal Server Error
```
500 Internal Server Error
```

**Solution:**
1. Check Flask server logs for the actual error
2. Look for Python exceptions in the terminal
3. Verify all imports are working

### Verification Steps

#### 1. Verify File Structure
```
SynaptixPhase2/
├── custom_ui/
│   ├── app.py (modified - has /rename-file route)
│   └── static/
│       └── script.js (modified - has async saveTestClassName)
└── generator_altUtl/
    ├── __init__.py (modified - exports rename functions)
    ├── file_rename_util.py (new)
    └── test_file_rename.py (new)
```

#### 2. Verify app.py has the route
```bash
grep -n "rename-file" c:\DATA\VS_Code_Notes\SynaptixPhase2\custom_ui\app.py
```

Should show:
```
597:@app.route('/rename-file', methods=['POST'])
```

#### 3. Verify import exists
```bash
grep -n "file_rename_util" c:\DATA\VS_Code_Notes\SynaptixPhase2\custom_ui\app.py
```

Should show:
```
22:from generator_altUtl.file_rename_util import rename_file_in_folder
```

### Quick Fix Commands

**Windows PowerShell:**
```powershell
# Navigate to project
cd c:\DATA\VS_Code_Notes\SynaptixPhase2

# Stop any running Flask servers (Ctrl+C)

# Start Flask server
cd custom_ui
python app.py
```

**Test the endpoint:**
```powershell
Invoke-WebRequest -Uri http://localhost:5000/rename-file `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"folder_name":"test","existing_file_name":"old","new_file_name":"new"}'
```

### Still Not Working?

If the issue persists:

1. **Check Flask logs** - Look at the terminal where Flask is running
2. **Check browser console** - Press F12 and look for errors
3. **Verify Python version** - Ensure Python 3.7+
4. **Check file permissions** - Ensure you can write to the project folder
5. **Clear browser cache** - Hard refresh with Ctrl+F5

### Debug Mode

Enable Flask debug mode for better error messages:

```python
# In app.py, at the bottom:
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

Restart the server and try again. You'll see detailed error messages.

### Contact Information

If you continue to experience issues:
1. Check the Flask server terminal for error messages
2. Check browser console (F12) for JavaScript errors
3. Verify all files were saved correctly
4. Ensure Flask server was restarted after changes
