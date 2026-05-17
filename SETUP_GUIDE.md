# DevLift Setup Guide

## Quick Setup Instructions

### 1. Backend Setup ✅ (In Progress)

The backend dependencies are currently being installed. Once complete:

```powershell
# Navigate to backend directory
cd backend

# The .env file has been created with your credentials
# Make sure to replace YOUR_NEW_ROTATED_WATSONX_API_KEY with your actual API key

# Start the backend server
python -m uvicorn main:app --reload
```

The backend will be available at: `http://localhost:8000`

Test it by visiting: `http://localhost:8000/health`

### 2. Frontend Setup (Next Step)

Open a **new terminal** and run:

```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start the development server
npm run dev
```

The frontend will be available at: `http://localhost:3000`

## Environment Variables

### Backend (`backend/.env`) ✅ Created

```env
WATSONX_API_KEY=YOUR_ACTUAL_API_KEY_HERE
WATSONX_PROJECT_ID=7f829f37-46cc-4fc5-bd11-f96a91d3a87c
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**Important**: Replace `YOUR_NEW_ROTATED_WATSONX_API_KEY` with your actual IBM watsonx.ai API key.

### Frontend (`.env.local`) - To be created

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Testing the Application

### 1. Test Backend Health

```powershell
# In a browser or using curl
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "ok",
  "model": "ibm/granite-34b-code-instruct"
}
```

### 2. Test Full Flow

1. Open `http://localhost:3000` in your browser
2. Paste a GitHub URL (e.g., `https://github.com/fastapi/fastapi`)
3. Click "Generate Kit"
4. Wait 20-40 seconds for the AI analysis
5. View the generated onboarding kit

## Troubleshooting

### Import Errors in VSCode

The red squiggly lines in VSCode are normal before dependencies are installed. They will disappear after:
- Backend: `pip install -r requirements.txt` completes
- Frontend: `npm install` completes

### Backend Won't Start

1. Check that Python 3.11+ is installed: `python --version`
2. Verify all dependencies installed: `pip list`
3. Check the `.env` file has your actual API key
4. Look for error messages in the terminal

### Frontend Won't Start

1. Check that Node.js 18+ is installed: `node --version`
2. Verify dependencies installed: `npm list`
3. Check `.env.local` exists with the correct API URL
4. Clear cache: `rm -rf .next` then `npm run dev`

### watsonx.ai API Errors

1. Verify your API key is correct in `backend/.env`
2. Check your IBM Cloud account has watsonx.ai access
3. Verify the project ID is correct
4. Check the region URL matches your IBM Cloud region

## Running Tests

### Backend Tests

```powershell
cd backend
pytest tests/ -v
```

### Manual API Testing

```powershell
# Test the analyze endpoint
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/fastapi/fastapi"}'
```

## Next Steps After Setup

1. ✅ Backend dependencies installed
2. ⏳ Replace API key in `backend/.env`
3. ⏳ Start backend server
4. ⏳ Install frontend dependencies
5. ⏳ Start frontend server
6. ⏳ Test the application
7. ⏳ Deploy to Railway (backend) and Vercel (frontend)

## Deployment

See the main README.md for detailed deployment instructions to:
- **Backend**: Railway (free tier)
- **Frontend**: Vercel (free tier)

## Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Review the main README.md
3. Check the terminal output for specific error messages
4. Verify all environment variables are set correctly