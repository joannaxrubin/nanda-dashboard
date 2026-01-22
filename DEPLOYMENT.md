# 🚀 Deployment Guide - NANDA Dashboard

## Option 1: Run Locally (Easiest - Start Here!)

### Step 1: Install Python
Make sure you have Python 3.9+ installed:
```bash
python --version
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the App
```bash
streamlit run nanda_dashboard_app.py
```

The app will open automatically at `http://localhost:8501`

**That's it! Your dashboard is running with sample data.**

---

## Option 2: Deploy to Streamlit Cloud (Free & Recommended)

This makes your dashboard accessible to your whole team from anywhere!

### Step 1: Push to GitHub

1. Create a new repository on GitHub
2. Push your dashboard code:

```bash
git init
git add .
git commit -m "Initial NANDA dashboard"
git remote add origin https://github.com/YOUR_USERNAME/nanda-dashboard.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Connect your GitHub repository
4. Set:
   - **Main file path**: `nanda_dashboard_app.py`
   - **Python version**: 3.9
5. Click "Deploy"

**Your dashboard will be live in ~2 minutes!**

You'll get a URL like: `https://your-app-name.streamlit.app`

### Step 3: Share with Team

Send the URL to your team members - they can access it from any device!

---

## Option 3: Connect to Live Notion Data

### Step 1: Create Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Click "+ New integration"
3. Name it "NANDA Dashboard"
4. Select your workspace
5. Click "Submit"
6. Copy the "Internal Integration Token"

### Step 2: Share Database with Integration

1. Open your NANDA Hackathon Task Tracker in Notion
2. Click "••• More" in top right
3. Click "Connections"
4. Click "+ Add connections"
5. Find and select "NANDA Dashboard"

### Step 3: Add Secrets to Streamlit

**For Local Development:**

Create `.streamlit/secrets.toml`:
```toml
NOTION_API_KEY = "secret_YOUR_TOKEN_HERE"
DATABASE_ID = "dc9611d2-af6d-4aa5-9a19-eb5f47aab9b9"
```

**For Streamlit Cloud:**

1. Go to your app dashboard on https://share.streamlit.io
2. Click "Settings" → "Secrets"
3. Add:
```toml
NOTION_API_KEY = "secret_YOUR_TOKEN_HERE"
DATABASE_ID = "dc9611d2-af6d-4aa5-9a19-eb5f47aab9b9"
```
4. Click "Save"

### Step 4: Update App Code

In `nanda_dashboard_app.py`, replace the `fetch_notion_tasks()` function:

```python
from notion_integration import NotionClient, get_sample_data

def fetch_notion_tasks():
    """Fetch tasks from Notion database"""
    try:
        api_key = st.secrets.get("NOTION_API_KEY", "")
        database_id = st.secrets.get("DATABASE_ID", "")
        
        if not api_key or not database_id:
            # Use sample data if Notion not configured
            return get_sample_data()
        
        # Use real Notion data
        client = NotionClient(api_key, database_id)
        response = client.query_database()
        return client.parse_tasks(response)
    except Exception as e:
        print(f"Error fetching Notion data: {e}")
        return get_sample_data()
```

**Now your dashboard shows live data from Notion!** ✨

---

## Option 4: Deploy to Heroku

### Prerequisites
- Heroku account (free tier works)
- Heroku CLI installed

### Step 1: Create Heroku Files

Create `Procfile`:
```
web: streamlit run nanda_dashboard_app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `runtime.txt`:
```
python-3.9.18
```

### Step 2: Deploy

```bash
heroku login
heroku create nanda-dashboard
git push heroku main
heroku config:set NOTION_API_KEY=your_key_here
heroku open
```

---

## Option 5: Run with Docker

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "nanda_dashboard_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
docker build -t nanda-dashboard .
docker run -p 8501:8501 nanda-dashboard
```

Open `http://localhost:8501`

---

## 🔐 Security Best Practices

1. **Never commit secrets to Git**
   - Add `.streamlit/secrets.toml` to `.gitignore`
   - Use environment variables or Streamlit secrets

2. **Keep your Notion token private**
   - Don't share in screenshots
   - Rotate if accidentally exposed

3. **Limit integration permissions**
   - Only share necessary databases with integration
   - Use read-only access if possible

---

## 📱 Mobile Access

Your Streamlit dashboard works great on mobile!

**For iOS/Android:**
1. Open the dashboard URL in mobile browser
2. Add to home screen for app-like experience
3. Pin to easily access during meetings

---

## 🎨 Customization After Deployment

### Update Team Colors

Edit in `nanda_dashboard_app.py`:
```python
.tech-team { border-left-color: #YOUR_COLOR; }
.outreach-team { border-left-color: #YOUR_COLOR; }
.events-team { border-left-color: #YOUR_COLOR; }
```

### Add Team Logo

Replace placeholder image URL:
```python
st.image("https://your-logo-url.com/logo.png", use_container_width=True)
```

### Change Countdown Dates

Update target dates:
```python
days_to_meeting = calculate_countdown("2024-12-18")  # Change date
days_to_presentation = calculate_countdown("2025-01-12")  # Change date
days_to_hackathon = calculate_countdown("2025-02-22")  # Change date
```

---

## 🔄 Updating Your Dashboard

### Local Development
1. Make changes to code
2. Save file
3. Streamlit auto-reloads!

### Streamlit Cloud
1. Push changes to GitHub
2. Streamlit Cloud auto-deploys
3. Refresh browser to see updates

### Heroku
```bash
git push heroku main
```

---

## 📊 Analytics & Monitoring

### Track Dashboard Usage (Optional)

Add Google Analytics:

```python
# In your app
st.markdown("""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR_GA_ID');
</script>
""", unsafe_allow_html=True)
```

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt --upgrade
```

### Dashboard won't load
- Check Python version (must be 3.9+)
- Verify all dependencies installed
- Check firewall isn't blocking port 8501

### Notion data not showing
- Verify API key is correct
- Check database is shared with integration
- Test with sample data first

### Streamlit Cloud deployment fails
- Check requirements.txt has all dependencies
- Verify Python version in settings
- Check app logs for specific errors

---

## 🎯 Quick Start Checklist

- [ ] Install Python 3.9+
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run locally: `streamlit run nanda_dashboard_app.py`
- [ ] Test with sample data ✅
- [ ] Create Notion integration (optional)
- [ ] Connect to live Notion data (optional)
- [ ] Deploy to Streamlit Cloud
- [ ] Share URL with team
- [ ] Celebrate! 🎉

---

## 💡 Pro Tips

1. **Start simple** - Deploy with sample data first, add Notion later
2. **Test locally** - Always test changes locally before deploying
3. **Mobile-first** - Check how it looks on phones during team meetings
4. **Screenshot wins** - Capture dashboard metrics for presentations
5. **Keep it updated** - Fresh data = engaged team

---

## 📞 Need Help?

**Streamlit Resources:**
- [Streamlit Docs](https://docs.streamlit.io)
- [Streamlit Community](https://discuss.streamlit.io)

**Notion API:**
- [Notion API Docs](https://developers.notion.com)
- [Integration Guide](https://developers.notion.com/docs/getting-started)

**This Project:**
- Check README.md for full documentation
- Review notion_integration.py for API examples

---

**Recommended Deployment Flow:**

1. **Week 1**: Run locally with sample data
2. **Week 2**: Deploy to Streamlit Cloud, share with team
3. **Week 3**: Connect to live Notion data
4. **Ongoing**: Update as project progresses

Good luck with your launch! 🚀
