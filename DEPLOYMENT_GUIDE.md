# CausalityCare Full Stack Deployment Guide

## 📋 Prerequisites
- ✅ GitHub account (you have this: ShrinikaTelu)
- ✅ Code pushed to GitHub (done)
- ⏳ Railway.app account (need to create)

---

## 🚀 Step-by-Step Deployment

### **Step 1: Deploy Backend to Railway (3 minutes)**

1. Go to **https://railway.app**
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Click **"Configure GitHub App"** to authorize Railway
5. Select **ShrinikaTelu/causalitycare** repo
6. Click **"Deploy Now"**

**Railway will automatically:**
- Detect the Dockerfile
- Build the container
- Deploy your FastAPI backend
- Give you a public URL like: `https://causalitycare-prod-abc123.up.railway.app`

**⏱️ Wait 2-5 minutes for deployment to finish**

---

### **Step 2: Test Backend Health Check**

Once Railway shows "Deployment Success", test it:

```bash
# Replace with your actual Railway URL
curl https://your-railway-url.up.railway.app/health

# Should return:
# {"status": "healthy", "multimodal_enabled": true, "version": "2.1.0"}
```

✅ **If you see this JSON, backend is deployed!**

---

### **Step 3: Deploy Frontend (5 minutes)**

Copy your Railway URL and run the deploy script:

```bash
cd /Users/shrinikatelu/causalitycare

# Run the deployment script
./deploy.sh

# Follow the prompts:
# 1. Enter your Railway URL when asked
# 2. Script will build & deploy frontend to GitHub Pages
```

**OR manually run these commands:**

```bash
# 1. Update the API endpoint in frontend
sed -i '' "s|'http://localhost:8000'|'https://your-railway-url.up.railway.app'|g" \
  frontend/src/app/services/causality.service.ts

# 2. Build production version
cd frontend
ng build --configuration production --base-href "/causalitycare/"

# 3. Deploy to GitHub Pages
npx angular-cli-ghpages --dir=dist/causalitycare
```

✅ **Your site will be live at: https://ShrinikaTelu.github.io/causalitycare/**

---

## ✅ Verify Everything Works

1. **Visit:** https://ShrinikaTelu.github.io/causalitycare/
2. **Enter text:** "I feel stressed"
3. **Click "Analyze"**
4. **Should get results in 15-20 seconds**

If it works → **You're done! 🎉**

---

## 🐛 Troubleshooting

### **Issue: "Failed to connect to API"**
- Check Railway deployment finished
- Verify Railway URL is correct in frontend code
- Check browser console (F12) for exact error
- Ensure Railway environment has `GEMINI_API_KEY` set

### **Issue: "Build failed"**
- Check backend logs on Railway dashboard
- Ensure Dockerfile is in `/backend/` folder
- Verify requirements.txt has all dependencies

### **Issue: "GitHub Pages not updating"**
- Force browser cache clear: `Cmd + Shift + R` (Mac)
- Wait 5 minutes for GitHub Pages to rebuild
- Check "Settings" → "Pages" → branch is set to `gh-pages`

---

## 📚 Project Links After Deployment

| Item | URL |
|------|-----|
| **Live App** | https://ShrinikaTelu.github.io/causalitycare/ |
| **Backend API** | https://your-railway-url.up.railway.app |
| **API Health** | https://your-railway-url.up.railway.app/health |
| **GitHub Repo** | https://github.com/ShrinikaTelu/causalitycare |

---

## 🎯 Next Steps After Deployment

1. **Test with your own data** (images, audio, text)
2. **Share the link:** https://ShrinikaTelu.github.io/causalitycare/
3. **Submit to Devpost** with live demo link
4. **Share on social media** 🚀

---

**Questions? Check:**
- Railway docs: https://docs.railway.app
- Angular deployment: https://angular.io/guide/deployment
- GitHub Pages: https://pages.github.com
