# Deployment Guide for PythonAnywhere

## Prerequisites

- PythonAnywhere account (free or paid)
- Your project files uploaded to PythonAnywhere

## Step-by-Step Deployment

### 1. Upload Your Project

1. Log into your PythonAnywhere account
2. Go to the "Files" tab
3. Upload your project files to `/home/yourusername/deep_research_agent/`
4. Or use git to clone: `git clone https://github.com/yourusername/deep_research_agent.git`

### 2. Create Virtual Environment

Open a Bash console in PythonAnywhere and run:

```bash
cd /home/yourusername/deep_research_agent
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Web App

1. Go to the "Web" tab in PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10
5. Set the following in the web app configuration:

**Source code:** `/home/yourusername/deep_research_agent`
**Working directory:** `/home/yourusername/deep_research_agent`
**WSGI configuration file:** Edit and replace content with:

```python
import sys
import os

# Add your project directory to the Python path
path = '/home/yourusername/deep_research_agent'
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application

if __name__ == "__main__":
    application.run()
```

**Virtual environment:** `/home/yourusername/deep_research_agent/venv`

### 4. Set Up Static Files (if needed)

In the "Static files" section:

- URL: `/static/`
- Directory: `/home/yourusername/deep_research_agent/static/`

### 5. Test and Deploy

1. Click "Reload" button on the Web tab
2. Visit your app at `https://yourusername.pythonanywhere.com`

## Important Notes

### Memory Considerations

- Free accounts have limited memory (512MB)
- The sentence-transformers and torch libraries are memory-intensive
- Consider using smaller models or upgrading to a paid account

### Model Optimization for Free Accounts

If you hit memory limits, modify `modules/retriever.py` to use a smaller model:

```python
# Change from 'all-MiniLM-L6-v2' to a smaller model
model_name='all-MiniLM-L12-v1'  # Even smaller: 'all-MiniLM-L12-v1'
```

### Data Directory

- Upload your data files to the `data/` directory
- The web interface will automatically detect and index them

### Troubleshooting

1. Check error logs in PythonAnywhere Web tab
2. Ensure all dependencies are installed in the virtual environment
3. Verify file paths in wsgi.py match your actual directory structure
4. For memory issues, consider upgrading to a paid account

### Alternative: Console-based Access

If web hosting doesn't work due to memory constraints, you can still run the original CLI version:

1. SSH into your PythonAnywhere account
2. Navigate to your project directory
3. Activate virtual environment
4. Run: `python main.py`
