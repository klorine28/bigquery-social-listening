# Google Cloud Service Account Setup Guide

## Prerequisites
- Google Cloud account
- Access to the project `sinnia-gnp` (or your own project)
- Billing enabled on the project

## Steps to Create Service Account Key

### 1. Access Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project (`sinnia-gnp` or create a new one)

### 2. Create Service Account
1. Navigate to **IAM & Admin** → **Service Accounts**
   - Or use direct link: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click **CREATE SERVICE ACCOUNT**
3. Fill in:
   - Service account name: `bigquery-reader` (or your preferred name)
   - Service account ID: (auto-generated)
   - Description: "Service account for BigQuery data access"
4. Click **CREATE AND CONTINUE**

### 3. Grant Permissions
Add these roles to the service account:
- **BigQuery Data Viewer** - To read data from tables
- **BigQuery Job User** - To run queries
- **BigQuery User** - To access datasets

Click **CONTINUE** → **DONE**

### 4. Create Key
1. Find your service account in the list
2. Click on the service account name
3. Go to **KEYS** tab
4. Click **ADD KEY** → **Create new key**
5. Choose **JSON** format
6. Click **CREATE**
7. The JSON key file will download automatically

### 5. Save the Key File
1. Save the downloaded JSON file to your project directory
2. Rename it to something like `service-account-key.json`
3. **IMPORTANT**: This file is already in `.gitignore` - never commit it!

## Using the Key

### Option 1: Environment Variable
Create a `.env` file in your project root:
```
GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json
GOOGLE_CLOUD_PROJECT=sinnia-gnp
```

### Option 2: Direct Path in Code
In your Jupyter notebooks:
```python
credentials_path = './service-account-key.json'
project_id = 'sinnia-gnp'
```

## Security Best Practices

1. **Never commit the JSON key** to version control
2. **Limit permissions** - Only grant necessary BigQuery roles
3. **Rotate keys regularly** - Delete old keys and create new ones
4. **Use different keys** for development and production
5. **Store securely** - Consider using secret management services for production

## Troubleshooting

### "Permission denied" errors
- Verify the service account has BigQuery Data Viewer role
- Check if the dataset/table has specific access controls

### "Project not found" errors
- Ensure you're using the correct project ID
- Verify billing is enabled on the project

### "Invalid credentials" errors
- Check the JSON file path is correct
- Ensure the JSON file is valid (not corrupted)
- Verify the service account still exists

## Alternative: Application Default Credentials
If you have gcloud CLI installed:
```bash
gcloud auth application-default login
```
This creates credentials in your user profile, useful for development.