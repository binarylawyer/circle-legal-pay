# Deploying Agent-Ledger to Vercel

## Quick Deploy (5 Minutes)

### **Prerequisites**
- Vercel account (sign up at https://vercel.com)
- Vercel CLI installed (optional but recommended)

---

## **Option 1: Deploy via Vercel Dashboard (Easiest)**

### **Step 1: Push to GitHub**
```bash
# Make sure all changes are committed and pushed
git add .
git commit -m "Add Vercel deployment configuration"
git push origin claude/build-repo-from-prompt-011CUvwUzDLq8EoUHgyB7n1y
```

### **Step 2: Import to Vercel**

1. Go to https://vercel.com/new
2. Click "Import Git Repository"
3. Select your GitHub repo: `binarylawyer/circle-legal-pay`
4. Select branch: `claude/build-repo-from-prompt-011CUvwUzDLq8EoUHgyB7n1y`
5. Configure project:
   - **Framework Preset:** Other
   - **Root Directory:** `./`
   - **Build Command:** (leave empty)
   - **Output Directory:** (leave empty)

### **Step 3: Add Environment Variables**

Click "Environment Variables" and add:

```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MOCK_MODE=True
ARC_RPC_URL=https://rpc.testnet.arc.network
ARC_CHAIN_ID=5042002
```

**Optional (for full functionality):**
```
CIRCLE_API_KEY=your_circle_api_key
CIRCLE_ENTITY_SECRET=your_circle_entity_secret
GEMINI_API_KEY=your_gemini_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

### **Step 4: Deploy**

1. Click "Deploy"
2. Wait 2-3 minutes
3. Get your live URL: `https://your-project.vercel.app`

---

## **Option 2: Deploy via Vercel CLI (Faster)**

### **Step 1: Install Vercel CLI**
```bash
npm i -g vercel
```

### **Step 2: Login**
```bash
vercel login
```

### **Step 3: Deploy**
```bash
cd /home/user/circle-legal-pay
vercel
```

Follow prompts:
- Set up and deploy? **Y**
- Which scope? (select your account)
- Link to existing project? **N**
- What's your project's name? **agent-ledger**
- In which directory is your code located? **./**
- Want to override settings? **N**

### **Step 4: Set Environment Variables**
```bash
vercel env add FLASK_ENV production
vercel env add SECRET_KEY your-secret-key
vercel env add MOCK_MODE True
```

### **Step 5: Deploy to Production**
```bash
vercel --prod
```

---

## **Important Notes**

### **Database on Vercel**

⚠️ SQLite won't work on Vercel (serverless functions are stateless).

**Options:**

1. **Use Supabase (Recommended):**
   ```bash
   # In Vercel environment variables, set:
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

2. **Use Vercel Postgres:**
   - Go to your project dashboard
   - Click "Storage" → "Create Database" → "Postgres"
   - Copy the connection string
   - Add as `DATABASE_URL` environment variable

3. **Demo Mode (No Persistence):**
   - Keep `MOCK_MODE=True`
   - Data won't persist between requests
   - Good enough for hackathon judging

### **File Storage on Vercel**

The `document_storage/` folder won't work on serverless.

**Solutions:**
- Keep `MOCK_MODE=True` (files stored in /tmp, won't persist)
- Or integrate real SharePoint with MS Graph API keys

---

## **Testing Your Deployment**

Once deployed:

1. **Visit your URL:** `https://your-project.vercel.app`
2. **Test the home page:** Should load with Bootstrap UI
3. **Test API status:** `https://your-project.vercel.app/legal/api/status`
4. **Register a test user** and try the workflow

---

## **Troubleshooting**

### **Build Fails**
- Check Vercel logs in the dashboard
- Ensure `api/index.py` exists
- Ensure `vercel.json` is valid

### **500 Error**
- Check function logs in Vercel dashboard
- Verify environment variables are set
- Check database connection if using Postgres

### **Import Errors**
- Ensure `requirements.txt` includes all dependencies
- Vercel auto-installs from `requirements.txt`

---

## **Custom Domain (Optional)**

1. Go to project settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

---

## **For Hackathon Submission**

Use the Vercel URL in your lablab.ai submission:
```
Demo URL: https://agent-ledger.vercel.app
GitHub: https://github.com/binarylawyer/circle-legal-pay
```

**Recommended:** Deploy with `MOCK_MODE=True` so judges can test without API keys!
