# Google Cloud CLI Authentication Setup

This guide shows how to use Google Cloud CLI for authentication instead of service account JSON files.

## Prerequisites
- Google Cloud account
- Access to the project `sinnia-gnp`

## Install Google Cloud CLI

### Windows
```powershell
# Download the installer from:
https://cloud.google.com/sdk/docs/install#windows

# Or use PowerShell:
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
```

### macOS
```bash
# Using Homebrew
brew install google-cloud-sdk

# Or download from:
https://cloud.google.com/sdk/docs/install#mac
```

### Linux/WSL
```bash
# Add the Cloud SDK distribution URI as a package source
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Update and install
sudo apt-get update && sudo apt-get install google-cloud-cli
```

## Setup Authentication

### 1. Initialize gcloud
```bash
gcloud init
```
This will:
- Ask you to log in to your Google account
- Select or create a project
- Set default compute region (optional)

### 2. Set Application Default Credentials
```bash
gcloud auth application-default login
```
This opens your browser to authenticate and creates credentials that BigQuery can use.

### 3. Set Default Project (Optional)
```bash
gcloud config set project sinnia-gnp
```

## Verify Setup

### Check Current Authentication
```bash
# See active account
gcloud auth list

# See current project
gcloud config get-value project

# Test BigQuery access
bq ls
```

### Test in Python
```python
from google.cloud import bigquery

# Client will automatically use Application Default Credentials
client = bigquery.Client()
print(f"Authenticated to project: {client.project}")
```

## Using in This Project

Once you've run `gcloud auth application-default login`, the notebooks and scripts will automatically use your credentials. No JSON files needed!

1. Run the authentication command:
   ```bash
   gcloud auth application-default login
   ```

2. Start Jupyter:
   ```bash
   uv run jupyter notebook
   ```

3. Open `social_listening_query.ipynb` and run - it will use your gcloud credentials

## Switching Between Projects

```bash
# List all projects you have access to
gcloud projects list

# Switch to a different project
gcloud config set project PROJECT_ID

# Or use project-specific commands
bq ls --project_id=PROJECT_ID
```

## Troubleshooting

### "Could not authenticate" errors
```bash
# Re-authenticate
gcloud auth application-default login --force
```

### "Permission denied" errors
Ensure your Google account has these roles in the project:
- BigQuery Data Viewer
- BigQuery Job User

Ask your project admin to grant these roles in IAM.

### "Default project not set" errors
```bash
# Set default project
gcloud config set project sinnia-gnp
```

## Advantages of CLI Auth

1. **No key management** - No JSON files to secure
2. **User-based access** - Uses your Google account permissions
3. **Easy switching** - Switch between projects easily
4. **Automatic refresh** - Tokens refresh automatically
5. **Better for development** - Ideal for local development

## For Production/Deployment

For production environments, you should still use service accounts. This CLI method is best for:
- Local development
- Jupyter notebooks
- Personal scripts
- Testing and debugging