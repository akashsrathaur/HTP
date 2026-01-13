# 🚀 Free Deployment Guide

## Privacy-Preserving Virtual Identity System

This guide shows you how to deploy the system completely **FREE** using various cloud platforms.

---

## 🎯 Recommended Free Deployment Stack

### Backend: **Render** (Free Tier)
### Frontend: **Netlify** or **Vercel** (Free Tier)
### Database: **SQLite** (included) or **Neon** (Free PostgreSQL)

---

## 📦 Option 1: Render + Netlify (Recommended)

### Backend Deployment on Render

**Free Tier**: 750 hours/month, auto-sleep after inactivity

#### Step 1: Prepare for Deployment

1. **Create `render.yaml`** in project root:

```yaml
services:
  - type: web
    name: vid-system-backend
    env: python
    region: oregon
    plan: free
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        value: sqlite+aiosqlite:///./vid_system.db
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: HMAC_SECRET_KEY
        generateValue: true
      - key: VID_EXPIRY_MINUTES
        value: 60
      - key: VID_USAGE_LIMIT
        value: 1
      - key: CORS_ORIGINS
        value: https://your-frontend.netlify.app,http://localhost:3000
```

#### Step 2: Deploy to Render

1. **Push to GitHub**:
```bash
cd HTP
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/vid-system.git
git push -u origin main
```

2. **Connect to Render**:
   - Go to https://render.com
   - Sign up (free)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml`
   - Click "Create Web Service"

3. **Get your backend URL**: `https://vid-system-backend.onrender.com`

#### Step 3: Update Frontend API URL

Edit `frontend/app.js`:
```javascript
const API_BASE_URL = 'https://vid-system-backend.onrender.com';
```

### Frontend Deployment on Netlify

**Free Tier**: Unlimited sites, 100GB bandwidth/month

#### Step 1: Prepare Frontend

Create `netlify.toml` in project root:
```toml
[build]
  publish = "frontend"
  
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

#### Step 2: Deploy to Netlify

**Option A: Drag & Drop**
1. Go to https://netlify.com
2. Sign up (free)
3. Drag the `frontend` folder to Netlify Drop
4. Done! Get URL like `https://your-site.netlify.app`

**Option B: GitHub Integration**
1. Push frontend to GitHub
2. Go to Netlify → "Add new site" → "Import from Git"
3. Select repository
4. Build settings:
   - Base directory: `frontend`
   - Publish directory: `frontend`
5. Deploy

#### Step 3: Update CORS on Backend

Update backend's CORS_ORIGINS environment variable on Render:
```
https://your-site.netlify.app
```

---

## 📦 Option 2: Railway (All-in-One)

**Free Tier**: $5 credit/month (enough for small apps)

### Deploy Backend

1. **Create `railway.json`**:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "cd backend && pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

2. **Deploy**:
   - Go to https://railway.app
   - Sign up with GitHub
   - "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add environment variables (Railway auto-generates PORT)
   - Deploy!

3. **Generate Domain**: Railway provides free subdomain

### Deploy Frontend

Same Railway project:
- Add new service
- Use static site builder
- Point to `frontend` directory

---

## 📦 Option 3: Vercel (Frontend) + Render (Backend)

### Frontend on Vercel

**Free Tier**: Unlimited sites, 100GB bandwidth

1. **Create `vercel.json`**:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

2. **Deploy**:
```bash
npm install -g vercel
cd HTP
vercel
```

Or use Vercel's GitHub integration.

---

## 📦 Option 4: Fly.io (Backend) + Netlify (Frontend)

**Free Tier**: 3 shared-cpu VMs, 3GB storage

### Deploy Backend on Fly.io

1. **Install Fly CLI**:
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Create `fly.toml`**:
```toml
app = "vid-system"
primary_region = "sjc"

[build]
  [build.args]
    PYTHON_VERSION = "3.10"

[env]
  PORT = "8000"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

3. **Create `Dockerfile`**:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

4. **Deploy**:
```bash
fly launch
fly deploy
```

---

## 🗄️ Database Options (Free)

### Option 1: SQLite (Default)
- ✅ Already included
- ✅ No setup needed
- ⚠️ Limited to single server
- ⚠️ Data lost on server restart (on some platforms)

### Option 2: Neon (PostgreSQL)
- ✅ Free tier: 512MB storage
- ✅ Persistent data
- ✅ Better for production

**Setup**:
1. Go to https://neon.tech
2. Create free account
3. Create database
4. Get connection string
5. Update `DATABASE_URL`:
```
postgresql+asyncpg://user:pass@host/dbname
```

### Option 3: Supabase (PostgreSQL)
- ✅ Free tier: 500MB storage
- ✅ Built-in auth (optional)

**Setup**:
1. Go to https://supabase.com
2. Create project
3. Get PostgreSQL connection string
4. Update `DATABASE_URL`

### Option 4: Railway PostgreSQL
- ✅ Included in Railway free tier
- ✅ Auto-configured

---

## 🔧 Environment Variables for Production

Set these on your hosting platform:

```bash
# Required
DATABASE_URL=sqlite+aiosqlite:///./vid_system.db  # or PostgreSQL URL
JWT_SECRET_KEY=<generate-random-32-char-string>
HMAC_SECRET_KEY=<generate-random-32-char-string>

# Optional (with defaults)
VID_EXPIRY_MINUTES=60
VID_USAGE_LIMIT=1
CORS_ORIGINS=https://your-frontend.netlify.app,https://your-frontend.vercel.app
```

**Generate secrets**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 📋 Deployment Checklist

### Before Deployment

- [ ] Push code to GitHub
- [ ] Update `API_BASE_URL` in `frontend/app.js`
- [ ] Generate secret keys
- [ ] Choose hosting platforms
- [ ] Create accounts (Render, Netlify, etc.)

### Backend Deployment

- [ ] Deploy to chosen platform
- [ ] Set environment variables
- [ ] Verify deployment: `curl https://your-backend.com/`
- [ ] Check API docs: `https://your-backend.com/docs`
- [ ] Test health endpoint: `https://your-backend.com/health`

### Frontend Deployment

- [ ] Update CORS on backend with frontend URL
- [ ] Deploy frontend
- [ ] Test registration flow
- [ ] Test VID generation
- [ ] Test public verification

### Post-Deployment

- [ ] Test complete user flow
- [ ] Verify QR code generation
- [ ] Test from mobile device
- [ ] Monitor for errors
- [ ] Set up uptime monitoring (optional)

---

## 🎯 Recommended Setup for Beginners

**Easiest Path**:

1. **Backend**: Render
   - Click-based deployment
   - Auto-detects Python
   - Free SSL
   - Auto-sleep (wakes on request)

2. **Frontend**: Netlify Drop
   - Drag & drop deployment
   - Instant deployment
   - Free SSL
   - CDN included

3. **Database**: SQLite (default)
   - No setup needed
   - Works out of the box

**Total Time**: ~15 minutes
**Total Cost**: $0

---

## 🚨 Important Notes

### Free Tier Limitations

**Render**:
- Auto-sleeps after 15 min inactivity
- First request after sleep takes ~30 seconds
- 750 hours/month (enough for 1 app)

**Netlify**:
- 100GB bandwidth/month
- 300 build minutes/month
- More than enough for this app

**Railway**:
- $5 credit/month
- Runs out if heavily used
- Good for testing

### Production Considerations

For real production use:
- [ ] Use PostgreSQL instead of SQLite
- [ ] Add Redis for rate limiting
- [ ] Set up monitoring (UptimeRobot - free)
- [ ] Add error tracking (Sentry - free tier)
- [ ] Use custom domain
- [ ] Enable HTTPS (auto on all platforms)
- [ ] Set up backups

---

## 📱 Quick Deploy Commands

### Deploy to Render (Backend)
```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Deploy to Render"
git push

# 2. Go to render.com and connect repo
# 3. Done!
```

### Deploy to Netlify (Frontend)
```bash
# Option 1: Drag & Drop
# Just drag the 'frontend' folder to netlify.com/drop

# Option 2: CLI
npm install -g netlify-cli
cd HTP/frontend
netlify deploy --prod
```

### Deploy to Vercel (Frontend)
```bash
npm install -g vercel
cd HTP
vercel --prod
```

---

## 🔗 Useful Links

- **Render**: https://render.com
- **Netlify**: https://netlify.com
- **Vercel**: https://vercel.com
- **Railway**: https://railway.app
- **Fly.io**: https://fly.io
- **Neon (PostgreSQL)**: https://neon.tech
- **Supabase**: https://supabase.com

---

## 🆘 Troubleshooting

### Backend won't start
- Check environment variables are set
- Verify `requirements.txt` is correct
- Check logs on hosting platform
- Ensure PORT is set correctly

### Frontend can't connect to backend
- Update `API_BASE_URL` in `frontend/app.js`
- Add frontend URL to backend CORS
- Check backend is running
- Verify HTTPS/HTTP match

### Database errors
- For SQLite: Ensure write permissions
- For PostgreSQL: Verify connection string
- Check database URL format

### CORS errors
- Add frontend URL to backend `CORS_ORIGINS`
- Include both http and https versions
- Redeploy backend after CORS changes

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ Public backend API
- ✅ Public frontend website
- ✅ Free SSL certificates
- ✅ Global CDN
- ✅ Automatic deployments (if using Git)

**Share your deployed app** and demonstrate privacy-preserving identity concepts to the world!

---

**Need help?** Check the logs on your hosting platform or refer to their documentation.
