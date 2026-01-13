# 🚀 Quick Deployment Reference Card

## Step-by-Step Deployment (Copy & Paste This)

### 1️⃣ Create PostgreSQL on Render
```
1. Go to: https://dashboard.render.com
2. Click: New + → PostgreSQL
3. Name: vid-system-db
4. Plan: Free
5. Click: Create Database
6. Copy: Internal Database URL
```

### 2️⃣ Deploy Backend
```
1. Go to your existing Web Service on Render
2. Click: Environment tab
3. Add variable:
   Key: DATABASE_URL
   Value: <paste Internal Database URL>
4. Ensure these exist:
   - JWT_SECRET_KEY (generate)
   - HMAC_SECRET_KEY (generate)
   - CORS_ORIGINS=*
5. Save → Auto redeploys
```

### 3️⃣ Update Frontend Code
```bash
# Edit frontend/app.js line 6:
const API_BASE_URL = 'https://YOUR-BACKEND.onrender.com';

# Commit:
git add frontend/app.js
git commit -m "Update API URL for production"
git push
```

### 4️⃣ Deploy Frontend to Netlify
```
Option A (Easiest):
1. Go to: https://app.netlify.com/drop
2. Drag frontend folder
3. Done!

Option B (Auto-updates):
1. Go to: https://app.netlify.com
2. New site → Import from Git
3. Select: akashsrathaur/HTP
4. Base directory: frontend
5. Deploy!
```

### 5️⃣ Update CORS
```
1. Back to Render → Environment
2. Update CORS_ORIGINS:
   https://YOUR-SITE.netlify.app,https://YOUR-BACKEND.onrender.com
3. Save
```

### 6️⃣ Test
```
1. Open: https://YOUR-SITE.netlify.app
2. Register → Verify → Generate VID
3. Logout → Login → Data should persist!
```

---

## 🔗 Important URLs

| What | Where |
|------|-------|
| Render Dashboard | https://dashboard.render.com |
| Netlify Dashboard | https://app.netlify.com |
| Your Backend | https://vid-system-backend.onrender.com |
| Your Frontend | https://your-site.netlify.app |
| API Docs | https://vid-system-backend.onrender.com/docs |

---

## ⚙️ Environment Variables (Render Backend)

```
DATABASE_URL=postgresql+asyncpg://viduser:password@dpg-xxxxx/vid_system
JWT_SECRET_KEY=<click Generate>
HMAC_SECRET_KEY=<click Generate>
VID_EXPIRY_MINUTES=60
VID_USAGE_LIMIT=1
CORS_ORIGINS=https://your-site.netlify.app,https://vid-system-backend.onrender.com
```

---

## 🐛 Quick Fixes

**Backend won't start?**
→ Check DATABASE_URL starts with `postgresql+asyncpg://`

**Frontend can't connect?**
→ Update API_BASE_URL in frontend/app.js

**CORS error?**
→ Add your Netlify URL to CORS_ORIGINS on Render

**Data disappears?**
→ You're using SQLite - switch to PostgreSQL URL

---

## ✅ Success Check

- [ ] /health returns {"status":"healthy"}
- [ ] /docs shows API documentation
- [ ] Frontend loads without errors
- [ ] Can register and login
- [ ] Data persists after logout
- [ ] VIDs work correctly

---

**Full Guide**: See DEPLOYMENT_GUIDE.md for detailed instructions
