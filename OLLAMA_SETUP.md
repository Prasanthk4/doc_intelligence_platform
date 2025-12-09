# Ollama Installation Guide

## Step 1: Download and Install Ollama

### Option A: Download from Website (Recommended)
1. Open your browser and go to: https://ollama.ai/download
2. Download the Windows installer
3. Run the installer and follow the prompts
4. Ollama will be installed to: C:\Users\<YourUsername>\AppData\Local\Programs\Ollama

### Option B: Using PowerShell (if winget is available)
```powershell
winget install Ollama.Ollama
```

## Step 2: Verify Installation

After installation, restart your terminal and run:
```powershell
ollama --version
```

You should see the version number.

## Step 3: Pull Llama 3.2 3B Model

```powershell
ollama pull llama3.2:3b
```

This will download the model (~2GB). It will be stored in Ollama's default location:
- Windows: C:\Users\<YourUsername>\.ollama\models

## Step 4: (Optional) Pull Mistral 7B for Deep Analysis

```powershell
ollama pull mistral:7b
```

This is larger (~4.1GB) but provides better accuracy.

## Step 5: Verify Models are Downloaded

```powershell
ollama list
```

You should see:
- llama3.2:3b
- mistral:7b (if you downloaded it)

## Step 6: Test Ollama

```powershell
ollama run llama3.2:3b "Hello, how are you?"
```

You should get a response from the model.

## Important Notes

⚠️ **Model Storage Location**: 
- Ollama models CANNOT be stored in custom locations like d:\ML
- They are managed by Ollama and stored in: C:\Users\<YourUsername>\.ollama\models
- This is by design for Ollama's model management system

✅ **Your Project Location**: 
- Your project code is in: d:\ML\document-intelligence-platform
- The models will be accessed by Ollama from their default location
- Your application will connect to Ollama via its API

## Troubleshooting

If `ollama` command is not recognized after installation:
1. Restart your terminal/PowerShell
2. Check if Ollama service is running in Task Manager
3. Restart the Ollama service if needed

## Next Steps

After Ollama is installed and models are pulled:
1. Navigate to project: `cd d:\ML\document-intelligence-platform`
2. Install Python dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run app.py`
