# 🚀 Kids Story Generator - Complete Backend Setup Guide

## 📋 Architecture Overview

```
Frontend (React)
    ↓
Backend (Node.js + Express)
    ↓
Database (Firebase Firestore)
    ↓
APIs:
  - Claude API (Story Generation)
  - Razorpay/Stripe (Payments)
  - SendGrid (Email)
  - AWS S3 (PDF Storage)
```

---

## 1️⃣ Database Setup (Firebase)

### Installation
```bash
npm install firebase firebase-admin
```

### Firebase Config (`.env`)
```
FIREBASE_API_KEY=your_api_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_bucket
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
```

### Firestore Collections

#### users
```json
{
  "uid": "unique_id",
  "email": "user@example.com",
  "name": "User Name",
  "subscription": "free|premium|pro",
  "storiesGenerated": 5,
  "storiesLimit": 5,
  "language": "hi|en",
  "createdAt": "timestamp",
  "updatedAt": "timestamp",
  "paymentId": "razorpay_id"
}
```

#### stories
```json
{
  "id": "story_id",
  "userId": "user_uid",
  "title": "Story Title",
  "character": "Character Name",
  "setting": "Setting Name",
  "action": "Action",
  "content": "Story text...",
  "pdfUrl": "https://s3.com/story.pdf",
  "language": "hi|en",
  "likes": 12,
  "downloads": 5,
  "createdAt": "timestamp",
  "isPublished": false
}
```

#### subscriptions
```json
{
  "userId": "user_uid",
  "plan": "free|premium|pro",
  "paymentId": "razorpay_id",
  "amount": 9900,
  "currency": "INR",
  "startDate": "timestamp",
  "endDate": "timestamp",
  "status": "active|cancelled|expired",
  "autoRenew": true
}
```

---

## 2️⃣ Backend API Setup (Node.js + Express)

### Installation
```bash
npm init -y
npm install express cors dotenv firebase-admin axios razorpay nodemailer
```

### `.env` File
```
PORT=5000
FIREBASE_ADMIN_KEY=path/to/serviceAccountKey.json
CLAUDE_API_KEY=your_claude_key
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
SENDGRID_API_KEY=your_sendgrid_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=your_bucket_name
```

### Main Server (server.js)

```javascript
const express = require('express');
const cors = require('cors');
const admin = require('firebase-admin');
const axios = require('axios');
const Razorpay = require('razorpay');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(cors());

// Initialize Firebase Admin
const serviceAccount = require(process.env.FIREBASE_ADMIN_KEY);
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});
const db = admin.firestore();

// Initialize Razorpay
const razorpay = new Razorpay({
  key_id: process.env.RAZORPAY_KEY_ID,
  key_secret: process.env.RAZORPAY_KEY_SECRET,
});

// ==================== AUTH ====================
app.post('/api/auth/signup', async (req, res) => {
  try {
    const { email, password, name, language } = req.body;
    
    const userRecord = await admin.auth().createUser({
      email,
      password,
      displayName: name,
    });

    // Create user document
    await db.collection('users').doc(userRecord.uid).set({
      uid: userRecord.uid,
      email,
      name,
      language: language || 'hi',
      subscription: 'free',
      storiesGenerated: 0,
      storiesLimit: 5,
      createdAt: admin.firestore.FieldValue.serverTimestamp(),
    });

    const token = await admin.auth().createCustomToken(userRecord.uid);
    res.json({ success: true, token, uid: userRecord.uid });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    // Use Firebase client SDK for login (call from frontend)
    res.json({ success: true, message: 'Use Firebase Auth SDK for login' });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// ==================== STORY GENERATION ====================
app.post('/api/stories/generate', async (req, res) => {
  try {
    const { uid, character, setting, action, language } = req.body;

    // Check user subscription limits
    const userDoc = await db.collection('users').doc(uid).get();
    const user = userDoc.data();

    if (user.storiesGenerated >= user.storiesLimit) {
      return res.status(403).json({ error: 'Story limit reached. Upgrade plan.' });
    }

    // Call Claude API
    const prompt = `Write a fun, magical story for kids (ages 5-8) in ${language === 'hi' ? 'Hindi' : 'English'}:\n- Character: ${character}\n- Setting: ${setting}\n- Action: ${action}\n\nMake it 3 paragraphs with simple, engaging words.`;

    const response = await axios.post('https://api.anthropic.com/v1/messages', {
      model: 'claude-sonnet-4-6',
      max_tokens: 600,
      messages: [{ role: 'user', content: prompt }],
    }, {
      headers: { 'x-api-key': process.env.CLAUDE_API_KEY },
    });

    const storyContent = response.data.content[0].text;

    // Save story to Firestore
    const storyRef = db.collection('stories').doc();
    await storyRef.set({
      id: storyRef.id,
      userId: uid,
      character,
      setting,
      action,
      title: `${character} in ${setting}`,
      content: storyContent,
      language,
      likes: 0,
      downloads: 0,
      isPublished: false,
      createdAt: admin.firestore.FieldValue.serverTimestamp(),
    });

    // Update user stories count
    await db.collection('users').doc(uid).update({
      storiesGenerated: admin.firestore.FieldValue.increment(1),
    });

    res.json({
      success: true,
      story: {
        id: storyRef.id,
        title: `${character} in ${setting}`,
        content: storyContent,
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/stories/:uid', async (req, res) => {
  try {
    const { uid } = req.params;
    const stories = await db.collection('stories')
      .where('userId', '==', uid)
      .orderBy('createdAt', 'desc')
      .limit(20)
      .get();

    const storiesList = stories.docs.map(doc => doc.data());
    res.json({ success: true, stories: storiesList });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==================== PAYMENTS ====================
app.post('/api/payment/create-order', async (req, res) => {
  try {
    const { uid, plan } = req.body;

    const plans = {
      premium: { amount: 9900, limit: -1 }, // Unlimited
      pro: { amount: 29900, limit: -1 },
    };

    if (!plans[plan]) {
      return res.status(400).json({ error: 'Invalid plan' });
    }

    const order = await razorpay.orders.create({
      amount: plans[plan].amount,
      currency: 'INR',
      receipt: `receipt_${uid}_${Date.now()}`,
      notes: {
        userId: uid,
        plan: plan,
      }
    });

    res.json({
      success: true,
      orderId: order.id,
      amount: order.amount,
      currency: order.currency,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/payment/verify', async (req, res) => {
  try {
    const { uid, orderId, paymentId, signature, plan } = req.body;

    // Verify signature
    const body = orderId + '|' + paymentId;
    const expectedSignature = require('crypto')
      .createHmac('sha256', process.env.RAZORPAY_KEY_SECRET)
      .update(body)
      .digest('hex');

    if (expectedSignature !== signature) {
      return res.status(400).json({ error: 'Invalid signature' });
    }

    // Save subscription
    const plans = { premium: -1, pro: -1 };
    
    await db.collection('subscriptions').add({
      userId: uid,
      plan,
      paymentId,
      orderId,
      amount: plan === 'premium' ? 9900 : 29900,
      currency: 'INR',
      startDate: admin.firestore.FieldValue.serverTimestamp(),
      endDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days
      status: 'active',
      autoRenew: true,
    });

    // Update user subscription
    await db.collection('users').doc(uid).update({
      subscription: plan,
      storiesLimit: plans[plan],
    });

    res.json({ success: true, message: 'Payment verified' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==================== PDF GENERATION ====================
const PDFDocument = require('pdfkit');
const AWS = require('aws-sdk');

const s3 = new AWS.S3({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
});

app.post('/api/stories/:storyId/export-pdf', async (req, res) => {
  try {
    const { storyId } = req.params;
    const story = await db.collection('stories').doc(storyId).get();
    const storyData = story.data();

    // Create PDF
    const doc = new PDFDocument();
    let buffer = Buffer.alloc(0);

    doc.on('data', (chunk) => {
      buffer = Buffer.concat([buffer, chunk]);
    });

    doc.on('end', async () => {
      // Upload to S3
      const params = {
        Bucket: process.env.AWS_S3_BUCKET,
        Key: `stories/${storyId}.pdf`,
        Body: buffer,
        ContentType: 'application/pdf',
      };

      await s3.upload(params).promise();
      const pdfUrl = `https://${process.env.AWS_S3_BUCKET}.s3.amazonaws.com/stories/${storyId}.pdf`;

      // Update story with PDF URL
      await db.collection('stories').doc(storyId).update({ pdfUrl });

      res.json({ success: true, pdfUrl });
    });

    // Build PDF content
    doc.fontSize(24).text(storyData.title, { align: 'center' });
    doc.fontSize(12).text(`Character: ${storyData.character}`);
    doc.fontSize(12).text(`Setting: ${storyData.setting}`);
    doc.moveDown();
    doc.fontSize(14).text(storyData.content, { align: 'justify' });
    doc.end();
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==================== PARENT DASHBOARD ====================
app.get('/api/parent/:uid/analytics', async (req, res) => {
  try {
    const { uid } = req.params;
    const stories = await db.collection('stories')
      .where('userId', '==', uid)
      .get();

    const analytics = {
      totalStories: stories.size,
      thisMonth: stories.docs.filter(d => {
        const created = d.data().createdAt.toDate();
        const now = new Date();
        return created.getMonth() === now.getMonth();
      }).length,
      mostUsedCharacter: getMostFrequent(stories.docs.map(d => d.data().character)),
      totalLikes: stories.docs.reduce((sum, d) => sum + d.data().likes, 0),
    };

    res.json({ success: true, analytics });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

function getMostFrequent(arr) {
  return arr.sort((a, b) => arr.filter(x => x === a).length - arr.filter(x => x === b).length).pop();
}

// ==================== START SERVER ====================
app.listen(process.env.PORT || 5000, () => {
  console.log(`✨ Server running on port ${process.env.PORT || 5000}`);
});
```

---

## 3️⃣ Deployment Options

### Option A: Vercel (Frontend)
```bash
npm install -g vercel
vercel deploy
```

### Option B: Railway/Render (Backend)
```bash
# Railway
npm install -g railway
railway link
railway deploy

# Or Render
# Connect GitHub repo directly
```

### Option C: Docker + AWS/GCP
```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5000
CMD ["node", "server.js"]
```

---

## 4️⃣ Payment Integration (Razorpay)

### Frontend Integration
```javascript
const initiatePayment = async (plan) => {
  const response = await fetch('/api/payment/create-order', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ uid, plan })
  });

  const { orderId, amount } = await response.json();

  const options = {
    key: 'YOUR_RAZORPAY_KEY_ID',
    amount,
    currency: 'INR',
    name: 'Story Magic',
    description: `Upgrade to ${plan}`,
    order_id: orderId,
    handler: async (response) => {
      await fetch('/api/payment/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          uid,
          orderId,
          paymentId: response.razorpay_payment_id,
          signature: response.razorpay_signature,
          plan
        })
      });
    }
  };

  const rzp = new Razorpay(options);
  rzp.open();
};
```

---

## 5️⃣ Email Notifications (SendGrid)

```javascript
const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

app.post('/api/email/welcome', async (req, res) => {
  const msg = {
    to: req.body.email,
    from: 'noreply@storiesofmagic.com',
    subject: 'Welcome to Story Magic! ✨',
    html: '<h1>Welcome!</h1><p>Start creating magical stories for your kids!</p>',
  };

  await sgMail.send(msg);
  res.json({ success: true });
});
```

---

## 6️⃣ Monitoring & Analytics

### Setup Sentry for Error Tracking
```bash
npm install @sentry/node
```

```javascript
const Sentry = require('@sentry/node');
Sentry.init({ dsn: process.env.SENTRY_DSN });
app.use(Sentry.Handlers.errorHandler());
```

### Firebase Analytics
```javascript
analytics.logEvent('story_generated', {
  character: character,
  setting: setting,
  language: language
});
```

---

## 7️⃣ Environment Checklist

- [ ] Firebase project created
- [ ] Razorpay account setup
- [ ] SendGrid API key
- [ ] AWS S3 bucket created
- [ ] Claude API key
- [ ] Environment variables set
- [ ] Database indices created
- [ ] Security rules configured
- [ ] Domain SSL certificate
- [ ] Email templates ready

---

## 📊 Revenue Projection

```
Assumptions:
- 10,000 active users/month
- 20% conversion to premium
- 5% conversion to pro

Monthly Revenue:
- Premium: 2,000 users × ₹99 = ₹1,98,000
- Pro: 500 users × ₹299 = ₹1,49,500
- Ads: 8,000 free users × ₹5 = ₹40,000
- Print books: ₹30,000

Total: ₹4,17,500/month = ₹50 lakhs/year 🚀
```

---

## 🎯 Launch Checklist

- [ ] App tested on iOS & Android
- [ ] Privacy policy & T&C ready
- [ ] Parent consent mechanism implemented
- [ ] GDPR/data protection compliant
- [ ] Premium features demo video
- [ ] Google Play Store submission
- [ ] App Store submission
- [ ] Facebook/Instagram ads campaign
- [ ] YouTube channel setup
- [ ] Email marketing list ready
