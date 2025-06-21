# 🚀 Deploy to Streamlit Cloud

## Steps:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Go to Streamlit Cloud:**
   - Visit: https://share.streamlit.io
   - Sign in with GitHub

3. **Create App:**
   - Click "New app"
   - Select your repository
   - Main file: `app.py`
   - Python version: 3.10

4. **Add API Key:**
   - Go to Settings → Secrets
   - Add:
   ```toml
   GOOGLE_API_KEY = "your_api_key_here"
   ```

5. **Deploy:**
   - Click "Deploy!"

## Files:
- ✅ `app.py` - Main app
- ✅ `requirements.txt` - Dependencies
- ✅ `packages.txt` - System packages
- ✅ `style.css` - Styling
- ✅ `setup.py` - Package setup
- ✅ `runtime.txt` - Python version 