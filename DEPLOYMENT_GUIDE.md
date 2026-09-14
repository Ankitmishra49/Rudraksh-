# 🚀 Complete Deployment Guide - Step by Step

---

## Phase 1: Pre-Launch Setup (Week 1-2)

### 1.1 Domain & Hosting

```bash
# Get domain (Google Domains, Namecheap, GoDaddy)
Website: www.kahaniojaaadu.com
API: api.kahaniojaaadu.com
Email: hello@kahaniojaaadu.com

# SSL Certificate (free with Vercel/Railway)
Automatic HTTPS setup
```

### 1.2 Firebase Setup

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Create project in Firebase Console
# https://console.firebase.google.com

# Initialize project
firebase init

# Enable:
- Firestore Database
- Authentication (Email/Password)
- Storage (for PDFs)
- Hosting
```

### 1.3 Razorpay Setup

1. **Create Account:** https://dashboard.razorpay.com
2. **Get API Keys:**
   - Key ID: rzp_live_xxxxx
   - Key Secret: (keep secret!)
3. **Setup Webhooks:**
   ```
   URL: https://api.kahaniojaaadu.com/api/webhook/razorpay
   Events: payment.authorized, payment.failed
   ```

### 1.4 Environment Variables (.env)

```env
# Firebase
REACT_APP_FIREBASE_API_KEY=AIza...
REACT_APP_FIREBASE_AUTH_DOMAIN=project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=project-id
REACT_APP_FIREBASE_STORAGE_BUCKET=project.appspot.com

# Claude API
REACT_APP_CLAUDE_API_KEY=sk-ant-...

# Razorpay
REACT_APP_RAZORPAY_KEY_ID=rzp_live_...

# Deployment
REACT_APP_API_URL=https://api.kahaniojaaadu.com
REACT_APP_ENVIRONMENT=production
```

---

## Phase 2: Frontend Deployment

### 2.1 Build Optimization

```bash
# Install dependencies
npm install

# Create optimized build
npm run build

# Check bundle size (target <3MB)
npm run analyze

# Test build locally
npm run preview
```

### 2.2 Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel deploy --prod

# Configure environment variables in Vercel dashboard
# Settings > Environment Variables

# Custom domain
vercel domains add kahaniojaaadu.com
```

### 2.3 Deploy to Netlify (Alternative)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=build

# Configure in dashboard
# Domain settings
# Environment variables
```

---

## Phase 3: Backend Deployment

### 3.1 Prepare Backend

```bash
# Create package.json for backend
npm init -y

# Install dependencies
npm install express cors dotenv firebase-admin axios razorpay

# Create server.js (see BACKEND_SETUP.md)

# Test locally
npm run dev
```

### 3.2 Deploy to Railway.app

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add service
railway service add

# Deploy
railway deploy

# Get URL
railway open
```

### 3.3 Deploy to Render.com

```bash
# Push code to GitHub
git init
git add .
git commit -m "Initial commit"
git push origin main

# Create account on render.com
# New > Web Service > Connect GitHub

# Configure:
- Build Command: npm install
- Start Command: node server.js
- Environment: Node
- Plan: Free/Paid

# Add environment variables
# Dashboard > Environment
```

### 3.4 Deploy to AWS EC2 (Advanced)

```bash
# Create EC2 instance
# Ubuntu 22.04, t2.micro (free tier)

# SSH into instance
ssh -i key.pem ubuntu@ec2-instance.amazonaws.com

# Update system
sudo apt update && sudo apt upgrade -y

# Install Node
curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Clone repo
git clone https://github.com/yourname/story-app.git
cd story-app

# Install dependencies
npm install

# Create .env file
nano .env
# Paste environment variables

# Install PM2 (process manager)
sudo npm install -g pm2

# Start app
pm2 start server.js --name "story-app"
pm2 startup
pm2 save

# Setup Nginx reverse proxy
sudo apt install nginx
sudo nano /etc/nginx/sites-available/default

# Configure Nginx
upstream backend {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name api.kahaniojaaadu.com;

    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Test and restart
sudo nginx -t
sudo systemctl restart nginx

# Add SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.kahaniojaaadu.com

# Auto-renew SSL
sudo systemctl enable certbot.timer
```

---

## Phase 4: Mobile App Deployment

### 4.1 Google Play Store

```bash
# Generate signed APK
cd android
./gradlew bundleRelease

# Sign app
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
  -keystore my-release-key.jks app.apk alias_name

# Verify signature
jarsigner -verify -verbose -certs app.apk

# Upload to Play Store
# Console > Create app > Upload APK/AAB

# Checklist:
- App title & description
- Screenshots (min 4)
- Feature graphic
- Privacy policy
- Contact info
- Category: Education/Kids

# Content rating form
# Age rating questionnaire
```

### 4.2 Apple App Store

```bash
# Generate iOS build
cd ios
pod install
xcodebuild -workspace app.xcworkspace \
  -scheme app -configuration Release -archivePath build/app.xcarchive

# Export IPA
xcodebuild -exportArchive -archivePath build/app.xcarchive \
  -exportOptionsPlist options.plist -exportPath build

# Upload to App Store Connect
# Xcode > Window > Organizer > Upload

# Checklist:
- App name & subtitle
- Keywords (5)
- Description
- Screenshots (min 2, max 5)
- Preview video
- Privacy policy
- Support URL
- Age rating
- Category: Education/Kids
```

---

## Phase 5: Database Migration

### 5.1 Firestore Security Rules

```firestore
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only access their own data
    match /users/{uid} {
      allow read, write: if request.auth.uid == uid;
    }

    // Stories - user can read/write own, everyone can read public
    match /stories/{document=**} {
      allow create: if request.auth != null;
      allow read: if request.auth.uid == resource.data.userId || resource.data.isPublished == true;
      allow update, delete: if request.auth.uid == resource.data.userId;
    }

    // Subscriptions - user can only see own
    match /subscriptions/{document=**} {
      allow read, write: if request.auth.uid == resource.data.userId;
    }
  }
}
```

### 5.2 Create Indexes

```bash
# Firestore automatically creates indexes, but optimize:
# Console > Firestore > Indexes

# Create composite indexes for:
- stories: userId + createdAt
- users: subscription + storiesGenerated
- subscriptions: userId + status
```

---

## Phase 6: CI/CD Pipeline

### 6.1 GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: npm install
      - run: npm run test
      - run: npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: vercel/action@master
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

### 6.2 Set GitHub Secrets

```bash
# In GitHub repo > Settings > Secrets

VERCEL_TOKEN = ...
VERCEL_ORG_ID = ...
VERCEL_PROJECT_ID = ...
FIREBASE_SERVICE_ACCOUNT = ...
RAZORPAY_KEY = ...
```

---

## Phase 7: Monitoring & Analytics

### 7.1 Error Tracking (Sentry)

```javascript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "https://...@sentry.io/...",
  environment: process.env.REACT_APP_ENVIRONMENT,
  tracesSampleRate: 1.0,
});
```

### 7.2 Firebase Analytics

Already enabled by default, view in:
- Firebase Console > Analytics
- Track events: story_generated, subscription_started, etc.

### 7.3 Google Analytics

```html
<!-- index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_ID');
</script>
```

---

## Phase 8: Performance Optimization

### 8.1 API Response Times

```bash
# Target: <200ms

# Monitor in:
- Firebase Console > Performance
- Sentry > Performance tab
- Backend logs
```

### 8.2 Image Optimization

```javascript
// Use Next.js Image component or similar
<img loading="lazy" src="..." alt="..." />
```

### 8.3 Code Splitting

```javascript
// React.lazy for route splitting
const CreateStory = React.lazy(() => import('./pages/CreateStory'));
```

---

## Phase 9: Post-Launch Checklist

- [ ] Website live & working
- [ ] API responding < 200ms
- [ ] Payment gateway tested
- [ ] Email notifications working
- [ ] All links functional
- [ ] Mobile responsive
- [ ] SSL certificate active
- [ ] Analytics collecting data
- [ ] Error tracking working
- [ ] Backups automated
- [ ] CDN configured
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Secrets not exposed in code
- [ ] Database backups scheduled

---

## Phase 10: Monitoring Dashboard Setup

### Daily Checks
```
Uptime: >99%
Error rate: <0.1%
API latency: <200ms
User signups: >50/day
Revenue: ₹growth
```

### Tools
- **Uptime:** UptimeRobot (free)
- **Analytics:** Firebase + Google Analytics
- **Errors:** Sentry
- **Performance:** Vercel Analytics
- **Database:** Firebase Console

---

## Emergency Procedures

### Database Recovery
```bash
# Firestore auto-backups every 24 hours
# Manual backup:
gcloud firestore export gs://bucket-name/backup

# Restore:
gcloud firestore import gs://bucket-name/backup
```

### Rollback Deployment
```bash
# Vercel
vercel rollback

# Railway
railway deployment rollback

# Manual: Revert to previous git commit
git revert <commit-hash>
git push
```

---

## Cost Estimation (Monthly)

```
Firebase:
- Firestore: ₹1,000-5,000 (pay-as-you-go)
- Storage: ₹500-2,000
- Hosting: ₹500

Claude API:
- ₹10-30/story generated
- If 5K stories/month = ₹50,000-150,000

Razorpay:
- 2% transaction fee = ₹4,000-20,000

Hosting:
- Vercel: ₹0-5,000 (free tier + overage)
- Railway: ₹0-2,000

Email (SendGrid):
- ₹1,000-5,000

Analytics & Monitoring:
- ₹2,000-5,000

Total: ₹70,000-190,000/month
```

---

## Launch Week Timeline

**Day 1:** Deploy all services
**Day 2:** Beta tester access
**Day 3:** App Store submission
**Day 4:** Monitor errors, fix bugs
**Day 5:** Launch marketing campaign
**Day 6-7:** Monitor metrics, optimize

---

## Support

- **Deployment Issues:** Check logs in respective console
- **Database:** Firebase documentation
- **Backend:** Node.js error messages
- **Payment:** Razorpay sandbox testing
- **Email:** SendGrid templates

**Emergency Contact:**
- Sentry alerts to Slack
- Uptime alerts to phone
- High error rate → page on-call

---

**Good luck! 🚀✨**
