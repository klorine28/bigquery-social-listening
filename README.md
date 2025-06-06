# Google Cloud BigQuery Project

A portable Python environment for querying Google BigQuery and exporting data to CSV files.

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
- Google Cloud account with BigQuery access

## GitHub Setup

### Create a New Repository on GitHub

1. Go to [GitHub](https://github.com) and create a new repository
2. Don't initialize with README, .gitignore, or license (we already have these)
3. Copy the repository URL (e.g., `https://github.com/yourusername/your-repo-name.git`)

### Connect to GitHub

```bash
# Add GitHub remote
git remote add origin https://github.com/yourusername/your-repo-name.git

# Push to GitHub
git push -u origin master
```

### Clone on Another Computer

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

## Complete Setup Guide

### Step 1: Install Prerequisites

#### 1.1 Install uv (Python Package Manager)
```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 1.2 Install Google Cloud CLI
- Download from: https://cloud.google.com/sdk/docs/install
- Follow the installation instructions for your operating system
- After installation, restart your terminal

### Step 2: Clone and Set Up the Repository

```bash
# Clone the repository
git clone <your-repo-url>
cd google-cloud-proj

# Install Python dependencies
uv sync
```

### Step 3: Configure Google Cloud Authentication

```bash
# 1. Authenticate with Google Cloud (opens browser)
gcloud auth application-default login

# 2. Set your default project
gcloud config set project sinnia-gnp  # Replace with your project ID

# 3. Verify authentication works
gcloud auth application-default print-access-token
```

### Step 4: Start Working with the Project

```bash
# ALWAYS use uv run to ensure correct environment
uv run jupyter notebook

# Open social_listening_query.ipynb in the browser
```

## Complete Initialization Checklist

- [ ] **uv installed**: Run `uv --version` to verify
- [ ] **Google Cloud CLI installed**: Run `gcloud --version` to verify
- [ ] **Repository cloned**: You're in the `google-cloud-proj` directory
- [ ] **Dependencies installed**: Run `uv sync` completed successfully
- [ ] **Google Cloud authenticated**: Run `gcloud auth application-default login`
- [ ] **Project configured**: Run `gcloud config set project YOUR_PROJECT_ID`
- [ ] **Jupyter started correctly**: Use `uv run jupyter notebook`

## Alternative: Service Account Authentication (For automation/production)

1. Create a service account in Google Cloud Console
2. Download the JSON key file
3. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
4. Update `.env` with your credentials:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
   GOOGLE_CLOUD_PROJECT=your-project-id
   ```

## Usage

### IMPORTANT: Virtual Environment Setup

This project uses `uv` to manage dependencies. You MUST use one of these methods:

#### Method 1: Using `uv run` (Recommended)

```bash
# Install dependencies first
uv sync

# Always prefix commands with 'uv run'
uv run jupyter notebook
uv run python main.py
```

#### Method 2: Activate Virtual Environment

```bash
# Install dependencies first
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
# or
.venv\Scripts\activate.ps1 # On Windows PowerShell

# Now you can run commands normally
jupyter notebook
python main.py

# When done, deactivate
deactivate
```

### Start Jupyter Notebook

**Always use one of these commands:**

```bash
# Recommended: Using uv run
uv run jupyter notebook

# Or if virtual environment is activated
jupyter notebook
```

Then open `social_listening_query.ipynb` or `bigquery_tutorial.ipynb`.

**⚠️ WARNING**: If you start Jupyter without `uv run` or without activating the virtual environment, you'll get import errors!

### Run Python Scripts

```bash
# Using uv run (recommended)
uv run python main.py

# Or with activated virtual environment
python main.py
```

### Use in Your Own Scripts

```python
from main import get_bigquery_client, query_to_csv

# Initialize client (using Google Cloud CLI auth)
client = get_bigquery_client(project_id="your-project-id")

# Run query and save to CSV
query = "SELECT * FROM `project.dataset.table` LIMIT 1000"
query_to_csv(client, query, "data/results.csv")
```

## Project Structure

```
google-cloud-proj/
├── .env.example              # Environment variable template
├── .gitignore               # Git ignore file
├── social_listening_query.ipynb  # Main notebook for queries
├── main.py                  # Helper functions
├── pyproject.toml           # Project dependencies
├── README.md                # This file
└── data/                    # CSV output directory (created automatically)

## Features

- Portable virtual environment that works on any machine
- Jupyter Notebook for interactive data analysis
- Helper functions for common BigQuery operations
- Automatic CSV export with support for large datasets
- Environment-based configuration

## Troubleshooting

### ImportError: cannot import name 'bigquery' from 'google.cloud'

This error means you're not using the virtual environment. Fix it by:

1. Close your Jupyter notebook or Python script
2. Run `uv sync` to install dependencies
3. Use `uv run jupyter notebook` or `uv run python script.py`

**Common mistake**: Running `jupyter notebook` directly instead of `uv run jupyter notebook`

### "Application Default Credentials not found" error

Run this command to authenticate:
```bash
gcloud auth application-default login
```

Or set up a service account as described in the setup section.

### Permission denied errors
Ensure your service account has the necessary BigQuery permissions (BigQuery Data Viewer, BigQuery Job User).

### Large query results
Use the `chunk_size` parameter in `query_to_csv()` function to handle large datasets efficiently.

## Security Notes

- Never commit your service account JSON file
- Keep your `.env` file private
- All sensitive files are already in `.gitignore`