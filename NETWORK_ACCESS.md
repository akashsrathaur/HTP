# 📱 Cross-Device Access Guide

## Your System is Now Accessible from Any Device!

### 🌐 Network Information

**Your Local IP**: `10.12.86.113`

**Backend API**: `http://10.12.86.113:8000`
**Frontend**: `http://10.12.86.113:3000`

---

## 📲 How to Access from Another Device

### Step 1: Ensure Same WiFi Network
Make sure both devices (your computer and the other device) are connected to the **same WiFi network**.

### Step 2: Access the Frontend
On your other device (phone, tablet, another computer), open a web browser and go to:

```
http://10.12.86.113:3000
```

### Step 3: Use the System
- Register/Login
- Verify identity
- Generate VIDs
- Scan QR codes

Everything will work exactly the same as on your main computer!

---

## 🔧 Technical Details

### Database
- **Type**: SQLite (file-based)
- **Location**: `backend/vid_system.db`
- **Portable**: ✅ Yes - all data stored locally

### Backend
- **Server**: Running on `0.0.0.0:8000` (accessible from network)
- **CORS**: Configured to allow all origins
- **Status**: Check at `http://10.12.86.113:8000/health`

### Frontend
- **Server**: Python HTTP server on port 3000
- **API URL**: Configured to use `10.12.86.113:8000`

---

## 🚨 Troubleshooting

### Can't Connect from Other Device?

1. **Check WiFi**: Both devices on same network?
2. **Check Firewall**: Mac firewall might be blocking connections
   - Go to System Preferences → Security & Privacy → Firewall
   - Allow incoming connections for Python

3. **Check Backend**: Is it running?
   ```bash
   curl http://10.12.86.113:8000/health
   ```
   Should return: `{"status":"healthy"}`

4. **Check Frontend**: Is it serving?
   ```bash
   lsof -ti:3000
   ```
   Should show a process ID

### IP Address Changed?

If your IP address changes (after reconnecting to WiFi):

1. Find new IP:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

2. Update `frontend/app.js`:
   ```javascript
   const API_BASE_URL = 'http://YOUR_NEW_IP:8000';
   ```

3. Restart servers

---

## 🔐 Security Note

**Local Network Only**: This setup is for local network access only. The system is NOT exposed to the internet, which is good for security.

**For Internet Access**: You would need to:
- Deploy to a cloud service (Render, Railway, etc.)
- Use HTTPS
- Configure proper security measures

---

## ✅ Current Status

- ✅ Backend running on network IP
- ✅ Frontend configured for network access
- ✅ SQLite database (portable)
- ✅ CORS enabled for all origins
- ✅ Ready for cross-device access

**Test it now**: Open `http://10.12.86.113:3000` on your phone!
