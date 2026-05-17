# DevLift - Quick Start Guide

## ⚡ Super Fast Setup (3 Steps)

### 1️⃣ Update Your API Key

Open `backend/.env` and replace the placeholder with your actual IBM watsonx.ai API key:

```env
WATSONX_API_KEY=your_actual_api_key_here
```

### 2️⃣ Start Backend (Terminal 1)

```powershell
# Option A: Use the startup script
.\start-backend.ps1

# Option B: Manual start
cd backend
python -m uvicorn main:app --reload
```

✅ Backend running at: http://localhost:8000

### 3️⃣ Start Frontend (Terminal 2)

```powershell
# Option A: Use the startup script
.\start-frontend.ps1

# Option B: Manual start
cd frontend
npm install
npm run dev
```

✅ Frontend running at: http://localhost:3000

## 🎯 Test It Out

1. Open http://localhost:3000
2. Paste a GitHub URL: `https://github.com/fastapi/fastapi`
3. Click "Generate Kit"
4. Wait 20-40 seconds
5. Explore your onboarding kit!

## 📝 What You Have

### Backend Files ✅
- `backend/main.py` - FastAPI server with /analyze endpoint
- `backend/github_fetcher.py` - Smart file selection from GitHub
- `backend/prompt_builder.py` - Prompt construction for AI
- `backend/bob_client.py` - IBM watsonx.ai integration
- `backend/.env` - Your credentials (already configured!)

### Frontend Files ✅
- `frontend/app/page.tsx` - Main application with 4 states
- `frontend/components/` - All UI components
- `frontend/types/kit.ts` - TypeScript interfaces
- `frontend/lib/api.ts` - Backend API client

## 🔧 Troubleshooting

### Backend won't start?
```powershell
# Check Python version (need 3.11+)
python --version

# Reinstall dependencies
cd backend
pip install -r requirements.txt
```

### Frontend won't start?
```powershell
# Check Node version (need 18+)
node --version

# Clear cache and reinstall
cd frontend
Remove-Item -Recurse -Force node_modules, .next
npm install
```

### Import errors in VSCode?
- These are normal before dependencies install
- They'll disappear after running the install commands
- You can ignore them - the code will run fine!

### API key not working?
1. Check you replaced `YOUR_NEW_ROTATED_WATSONX_API_KEY` in `backend/.env`
2. Verify your IBM Cloud account has watsonx.ai access
3. Check the project ID is correct: `7f829f37-46cc-4fc5-bd11-f96a91d3a87c`

## 📚 More Help

- **Full Setup Guide**: See `SETUP_GUIDE.md`
- **Complete Documentation**: See `README.md`
- **API Documentation**: http://localhost:8000/docs (when backend is running)

## 🚀 Next Steps

1. ✅ Backend dependencies installed
2. ⏳ Update API key in `backend/.env`
3. ⏳ Start backend server
4. ⏳ Start frontend server
5. ⏳ Test with a GitHub repo
6. ⏳ Deploy to production (Railway + Vercel)

---

**Need help?** Check the troubleshooting section above or review the full documentation in README.md