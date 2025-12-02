# Deployment Instructions for CareEnforced AI

Your code has been successfully pushed to: https://github.com/christopheroueis/IAI-final

## Option 1: Deploy to Render (Recommended - Full Stack)

Render can host both your backend (FastAPI) and frontend (React/Vite) together.

### Steps:

1. **Sign up at Render**: https://render.com (use your GitHub account)

2. **Deploy Backend**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repo: `christopheroueis/IAI-final`
   - Configure:
     - **Name**: `careenforced-backend`
     - **Root Directory**: `backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Click "Create Web Service"
   - Note the URL (e.g., `https://careenforced-backend.onrender.com`)

3. **Deploy Frontend**:
   - Click "New +" → "Static Site"
   - Connect the same repo
   - Configure:
     - **Name**: `careenforced-frontend`
     - **Root Directory**: `frontend`
     - **Build Command**: `npm install && npm run build`
     - **Publish Directory**: `dist`
   - **Environment Variables**: Add `VITE_API_URL` = `https://careenforced-backend.onrender.com`
   - Click "Create Static Site"

4. **Update Frontend API URL**:
   - In your local `frontend/src/pages/HospitalInput.jsx` and `frontend/src/api.js`
   - Replace `http://localhost:8000` with your Render backend URL
   - Commit and push changes

5. **Your App is Live!**
   - Frontend URL: `https://careenforced-frontend.onrender.com`

## Option 2: Deploy to Vercel (Frontend) + Render (Backend)

### Backend (Render):
Same as Option 1, steps 1-2.

### Frontend (Vercel):

1. **Sign up at Vercel**: https://vercel.com (use GitHub)

2. **Import Project**:
   - Click "Add New" → "Project"
   - Import `christopheroueis/IAI-final`
   - Configure:
     - **Framework Preset**: Vite
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`
   - **Environment Variables**:
     - `VITE_API_URL` = your Render backend URL

3. **Deploy**: Click "Deploy"

4. **Your App is Live!**
   - Vercel will give you a URL like: `https://iai-final.vercel.app`

## Option 3: GitHub Pages (Frontend Only)

⚠️ **Note**: GitHub Pages can only host static sites. You'll still need Render/Railway for the backend.

1. **Deploy Backend** on Render (see Option 1)

2. **Update Frontend**:
   ```bash
   cd frontend
   # Update API URLs to point to your Render backend
   # Edit src/api.js and src/pages/HospitalInput.jsx
   ```

3. **Add GitHub Pages deployment script** to `package.json`:
   ```json
   {
     "scripts": {
       "deploy": "npm run build && gh-pages -d dist"
     }
   }
   ```

4. **Install gh-pages**:
   ```bash
   npm install --save-dev gh-pages
   ```

5. **Deploy**:
   ```bash
   npm run deploy
   ```

6. **Enable GitHub Pages**:
   - Go to repo Settings → Pages
   - Source: `gh-pages` branch
   - Your site: `https://christopheroueis.github.io/IAI-final/`

## Important: Update CORS Settings

Once deployed, update `backend/main.py` to allow your frontend domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-url.onrender.com",
        "https://iai-final.vercel.app",
        # Add your deployed frontend URL here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Recommended: Option 1 (Render)

**Why?** 
- ✅ Both frontend and backend on same platform
- ✅ Free tier available
- ✅ Automatic deploys from GitHub
- ✅ Easy environment variable management
- ✅ Built-in SSL certificates

**Your public URL will be**:
🌐 `https://careenforced-frontend.onrender.com`

## Next Steps After Deployment

1. Test both hospital and long-term care prediction flows
2. Share the public URL!
3. Monitor usage on Render dashboard
4. Consider upgrading to paid tier for better performance (if needed)

---

**Need Help?**
- Render docs: https://render.com/docs
- Vercel docs: https://vercel.com/docs
