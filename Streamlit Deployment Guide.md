# Streamlit Deployment Guide

**Digital Twin Dashboard - CAT C4.4 Engine**  
**Author:** Noah Aniah

---

## QUICK DEPLOYMENT CHECKLIST

Before pushing to GitHub and deploying to Streamlit Cloud:

### Files Check
- [x] `app.py` exists in root directory
- [x] `requirements.txt` has all packages
- [x] `.streamlit/config.toml` is configured
- [x] `.gitignore` is present
- [x] `README.md` is complete
- [x] `utils/helpers.py` is present
- [x] `utils/__init__.py` is present

### Code Quality
- [x] No hardcoded paths (use relative paths)
- [x] No API keys in code (use secrets)
- [x] All imports are in `requirements.txt`
- [x] Code runs locally without errors
- [x] `streamlit run app.py` works locally

### GitHub
- [x] Repository is public
- [x] All files committed
- [x] No large files (>100MB)
- [x] `.gitignore` prevents sensitive files
- [x] README is clear and complete

---

## STEP-BY-STEP DEPLOYMENT

### Step 1: Prepare Your Local Repository

```bash
# Navigate to project directory
cd streamlit_digital_twin

# Initialize git (if not already done)
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Check that all required files exist
ls -la
# Should show: app.py, requirements.txt, .gitignore, README.md, .streamlit/

# Verify structure
tree -L 2
# Should show proper directory structure
```

### Step 2: Test Locally

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Test in browser at http://localhost:8501
# Verify all pages work:
# - Dashboard
# - Real-Time Monitoring
# - Analytics
# - Documentation
# - About Developer

# Stop the app
# Press Ctrl+C in terminal
```

### Step 3: Commit to Git

```bash
# Check status
git status

# Add all files
git add .

# Commit with message
git commit -m "Initial commit: Digital Twin Dashboard - Built by Noah Aniah"

# Verify commit
git log --oneline
```

### Step 4: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `digital-twin-cat-c44`
3. Description: "Digital Twin Dashboard for CAT C4.4 Engine - Master's Thesis Project"
4. Make it **PUBLIC**
5. Click "Create repository"

### Step 5: Push to GitHub

```bash
# Add remote origin
git remote add origin https://github.com/yourusername/digital-twin-cat-c44.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main

# Verify on GitHub
# Go to https://github.com/yourusername/digital-twin-cat-c44
# Should see all your files
```

### Step 6: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit [streamlit.io/cloud](https://streamlit.io/cloud)
   - Sign in with GitHub account

2. **Create New App:**
   - Click "New app" button
   - Select "From existing repo"

3. **Configure Deployment:**
   - **Repository:** yourusername/digital-twin-cat-c44
   - **Branch:** main
   - **Main file path:** app.py

4. **Click "Deploy"**
   - Streamlit Cloud will:
     - Clone your repository
     - Install dependencies from requirements.txt
     - Run your app
     - Provide a public URL

5. **Wait for Deployment:**
   - Takes 2-5 minutes
   - You'll see deployment logs
   - App will be available at: `https://[your-app-name].streamlit.app`

### Step 7: Verify Deployment

1. **Check App URL:**
   - Visit: `https://[your-app-name].streamlit.app`
   - Should load the dashboard

2. **Test All Pages:**
   - Click through all navigation items
   - Verify charts load
   - Check metrics display correctly

3. **Check Logs:**
   - In Streamlit Cloud dashboard
   - Look for any errors or warnings
   - Should see "App is running"

---

## TROUBLESHOOTING

### Issue: "ModuleNotFoundError: No module named 'xxx'"

**Cause:** Package not in requirements.txt

**Solution:**
```bash
# 1. Add package to requirements.txt
echo "package-name==version" >> requirements.txt

# 2. Test locally
pip install -r requirements.txt
streamlit run app.py

# 3. Commit and push
git add requirements.txt
git commit -m "Add missing package"
git push origin main

# 4. Streamlit Cloud auto-redeploys
```

### Issue: "App won't deploy"

**Cause:** Syntax error or missing file

**Solution:**
```bash
# 1. Check syntax
python -m py_compile app.py

# 2. Verify all imports work
python -c "from utils.helpers import *"

# 3. Check file sizes
du -h *

# 4. Review Streamlit Cloud logs
# Look for specific error messages
```

### Issue: "Import errors after deployment"

**Cause:** Package version mismatch

**Solution:**
```bash
# 1. Pin specific versions in requirements.txt
# Change: streamlit>=1.28.0
# To: streamlit==1.28.1

# 2. Test locally with exact versions
pip install -r requirements.txt
streamlit run app.py

# 3. Commit and push
git add requirements.txt
git commit -m "Pin package versions"
git push origin main
```

### Issue: "App is too slow"

**Cause:** Expensive computations or large data

**Solution:**
```python
# Use Streamlit caching
@st.cache_data
def load_data():
    # This runs once, then cached
    return expensive_computation()

# Or use session state
if 'data' not in st.session_state:
    st.session_state.data = expensive_computation()
```

### Issue: "Can't connect to GitHub"

**Cause:** SSH key or authentication issue

**Solution:**
```bash
# Use HTTPS instead of SSH
git remote set-url origin https://github.com/yourusername/digital-twin-cat-c44.git

# Or configure SSH keys
ssh-keygen -t ed25519 -C "your.email@example.com"
# Add public key to GitHub settings
```

---

## UPDATING YOUR APP

After initial deployment, to make updates:

```bash
# 1. Make changes locally
# Edit files as needed

# 2. Test locally
streamlit run app.py

# 3. Commit changes
git add .
git commit -m "Description of changes"

# 4. Push to GitHub
git push origin main

# 5. Streamlit Cloud auto-redeploys
# Check deployment status in Streamlit Cloud dashboard
```

---

## MONITORING YOUR APP

### In Streamlit Cloud Dashboard

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Click on your app
3. View:
   - **Status:** Running/Stopped
   - **Logs:** Real-time application logs
   - **Settings:** Configuration options
   - **Secrets:** Environment variables

### Viewing Logs

```bash
# Local logs
tail -f ~/.streamlit/logs/streamlit.log

# Cloud logs
# View in Streamlit Cloud dashboard
# Click "Logs" tab
```

---

## SHARING YOUR APP

### Public URL

Your app is publicly available at:
```
https://[your-app-name].streamlit.app
```

### For Your Thesis

Include in your thesis document:

```
The Digital Twin Dashboard is deployed and publicly accessible at:
https://[your-app-name].streamlit.app

The application provides interactive visualization of the Digital Twin framework,
including real-time sensor monitoring, ML model performance metrics, RUL predictions,
and maintenance recommendations for the Caterpillar C4.4 engine.
```

### Share with Others

- **Direct URL:** Share the Streamlit Cloud URL
- **GitHub Link:** Share repository for code review
- **QR Code:** Generate QR code for the URL
- **Embed:** Can embed in websites (with limitations)

---

## BEST PRACTICES

### 1. Version Control

```bash
# Use meaningful commit messages
git commit -m "Add real-time monitoring page"
git commit -m "Fix: Correct RUL calculation formula"
git commit -m "Update: Improve performance with caching"

# Use branches for major changes
git checkout -b feature/new-page
# Make changes
git commit -m "Add new analytics page"
git push origin feature/new-page
# Create pull request on GitHub
```

### 2. Dependencies Management

```bash
# Keep requirements.txt updated
pip freeze > requirements.txt

# Pin specific versions
streamlit==1.28.1  # Good
streamlit>=1.28.0  # Bad (can break)

# Test with exact versions
pip install -r requirements.txt
```

### 3. Code Quality

```bash
# Use meaningful variable names
# Add comments for complex logic
# Keep functions small and focused
# Handle errors gracefully
```

### 4. Security

```bash
# Never commit secrets
# Use .streamlit/secrets.toml for API keys
# Add to .gitignore
# Use environment variables in Streamlit Cloud
```

---

## ADVANCED DEPLOYMENT OPTIONS

### Custom Domain

In Streamlit Cloud dashboard:
1. Go to App settings
2. Click "Custom domain"
3. Enter your domain
4. Follow DNS setup instructions

### Private Deployment

For private access:
1. Deploy to Heroku, AWS, or Azure
2. Use authentication layer
3. Restrict access to specific users

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py"]
```

```bash
# Build and run
docker build -t digital-twin .
docker run -p 8501:8501 digital-twin
```

---

## MAINTENANCE

### Regular Updates

```bash
# Update dependencies periodically
pip list --outdated

# Update requirements.txt
pip freeze > requirements.txt

# Test thoroughly
streamlit run app.py

# Commit and push
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

### Monitoring Performance

- Check Streamlit Cloud logs regularly
- Monitor app usage and errors
- Optimize slow pages
- Update ML models with new data

---

## FINAL CHECKLIST

Before submitting thesis:

- [ ] App deployed successfully
- [ ] All pages working correctly
- [ ] URL included in thesis
- [ ] GitHub repository is public
- [ ] README is complete
- [ ] Code is well-commented
- [ ] No sensitive data in code
- [ ] Screenshots captured for Chapter 4
- [ ] Deployment guide documented

---

**Your Streamlit app is ready to deploy!** 🚀

*Author: Noah Aniah*  
*Digital Twin Framework for CAT C4.4 Engine*
