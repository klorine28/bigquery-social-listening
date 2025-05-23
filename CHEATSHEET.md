# BigQuery Project Cheat Sheet

## Quick Start
```bash
# Navigate to project
cd /mnt/d/google_cloud_proj

# Start Jupyter with credentials
GOOGLE_APPLICATION_CREDENTIALS=~/.config/gcloud/application_default_credentials.json uv run jupyter notebook
```

## Environment Management

### Start Virtual Environment
```bash
# Option 1: Run commands with uv (recommended)
uv run python script.py
uv run jupyter notebook

# Option 2: Activate virtual environment manually
source .venv/bin/activate  # Linux/Mac/WSL
# or
.venv\Scripts\activate  # Windows Command Prompt
# or
.venv\Scripts\Activate.ps1  # Windows PowerShell
```

### Exit Virtual Environment
```bash
deactivate  # If you activated it manually
# or just close the terminal
```

### Update Dependencies
```bash
# After adding to pyproject.toml
uv sync

# Install specific package
uv add package-name
```

## Google Cloud CLI

### Authentication
```bash
# Initial login (do this in Windows, not WSL)
gcloud auth login
gcloud auth application-default login

# Copy credentials to WSL (if using WSL)
mkdir -p ~/.config/gcloud
cp /mnt/c/Users/YOUR_USERNAME/AppData/Roaming/gcloud/application_default_credentials.json ~/.config/gcloud/
```

### Project Management
```bash
# List all projects
gcloud projects list

# Set default project
gcloud config set project sinnia-gnp

# Show current project
gcloud config get-value project

# Show current authenticated account
gcloud auth list
```

### BigQuery Commands
```bash
# List datasets
bq ls

# List tables in a dataset
bq ls social_dashboard_table

# Show table schema
bq show sinnia-gnp:social_dashboard_table.listening_table_prd

# Run a query from command line
bq query --use_legacy_sql=false 'SELECT COUNT(*) FROM `sinnia-gnp.social_dashboard_table.listening_table_prd`'

# Export query results to CSV
bq query --use_legacy_sql=false --format=csv 'YOUR_QUERY_HERE' > output.csv
```

## Git Commands

### Daily Workflow
```bash
# Check status
git status

# Add and commit changes
git add .
git commit -m "Your message"

# Push to GitHub
git push

# Pull latest changes
git pull
```

### Common Operations
```bash
# See commit history
git log --oneline

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Merge branch
git checkout main
git merge feature-name
```

## Jupyter Shortcuts

### Command Mode (press Esc)
- `A` - Insert cell above
- `B` - Insert cell below
- `DD` - Delete cell
- `M` - Change to Markdown
- `Y` - Change to Code

### Edit Mode (press Enter)
- `Shift + Enter` - Run cell and move to next
- `Ctrl + Enter` - Run cell and stay
- `Alt + Enter` - Run cell and insert below

### Other
- `Kernel → Restart & Run All` - Restart and run entire notebook
- `File → Download as → HTML/PDF` - Export notebook

## Project-Specific Commands

### Run the main script
```bash
uv run python main.py
```

### Run a specific query and save to CSV
```python
from main import get_bigquery_client, query_to_csv

client = get_bigquery_client()
query = "SELECT * FROM `sinnia-gnp.social_dashboard_table.listening_table_prd` LIMIT 100"
query_to_csv(client, query, "data/test_export.csv")
```

## Troubleshooting

### WSL Jupyter can't find credentials
```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/.config/gcloud/application_default_credentials.json
```

### Permission denied errors
```bash
# Check your roles
gcloud projects get-iam-policy sinnia-gnp --filter="bindings.members:YOUR_EMAIL"
```

### Jupyter won't start
```bash
# Kill existing Jupyter processes
pkill jupyter

# Start fresh
uv run jupyter notebook
```

### Git push authentication failed
```bash
# Update remote URL with new token
git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/YOUR_USERNAME/REPO_NAME.git
```

## Environment Variables (.env file)
```bash
# Create from template
cp .env.example .env

# Edit with nano (in terminal)
nano .env

# Or with VS Code
code .env
```

## Quick Data Export (One-liner)
```bash
# Export today's data
uv run python -c "from main import *; client = get_bigquery_client(); query_to_csv(client, 'SELECT * FROM \`sinnia-gnp.social_dashboard_table.listening_table_prd\` WHERE DATE(created_at) = CURRENT_DATE() LIMIT 1000', 'data/today_export.csv')"
```