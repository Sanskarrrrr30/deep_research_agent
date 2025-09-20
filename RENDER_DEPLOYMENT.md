# Deployment Guide for Render

## Prerequisites

- GitHub account with your project repository
- Render account (free tier available)
- Your project pushed to GitHub with all necessary files

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure your GitHub repository contains these files:
- `app.py` - Flask web application
- `requirements.txt` - Python dependencies including gunicorn
- `render.yaml` - Render service configuration
- `modules/` - Your application modules
- `data/` - Your document files
- `templates/` - HTML templates

### 2. Deploy on Render

1. **Sign up/Login to Render**
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository: `Sanskarrrrr30/deep_research_agent`

3. **Configure Service Settings**
   - **Name**: `deep-research-agent` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Plan**: Select `Free` (512MB RAM, sleeps after 15min inactivity)

4. **Environment Variables** (Optional)
   - No additional environment variables needed for basic setup

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app
   - Build process takes 5-10 minutes

### 3. Access Your Application

- Your app will be available at: `https://your-app-name.onrender.com`
- Example: `https://deep-research-agent.onrender.com`

### 4. Upload Data Files

Since Render rebuilds from scratch on each deploy, you have two options for data files:

#### Option A: Include in Repository (Recommended for small files)
```bash
# Add your data files to git and push
git add data/
git commit -m "Add data files"
git push origin main
```

#### Option B: Use External Storage (for large files)
- Use cloud storage (Google Drive, Dropbox, S3)
- Modify your app to download files on startup
- Store URLs in environment variables

## Important Notes

### Free Tier Limitations

- **Memory**: 512MB RAM limit
- **Sleep**: App sleeps after 15 minutes of inactivity
- **Build Time**: 15-minute build timeout
- **Bandwidth**: 100GB/month

### Memory Optimization

The sentence-transformers and torch libraries are memory-intensive. If you hit memory limits:

1. **Use Smaller Models**: Modify `modules/retriever.py`:
```python
# Use a smaller model
model_name='all-MiniLM-L12-v2'  # ~120MB instead of ~400MB
```

2. **Lazy Loading**: Models are loaded only when needed (already implemented)

3. **Consider Upgrading**: Render's paid plans start at $7/month with 512MB+ RAM

### Auto-Deploy

- Render automatically redeploys when you push to your main branch
- Check deployment logs in Render dashboard for any issues

### Troubleshooting

1. **Build Failures**
   - Check build logs in Render dashboard
   - Verify all dependencies are in requirements.txt
   - Ensure Python version compatibility

2. **Memory Issues**
   - Use smaller ML models
   - Consider upgrading to paid plan
   - Monitor resource usage in Render dashboard

3. **App Not Loading**
   - Check service logs for errors
   - Verify Flask app is binding to correct port
   - Ensure all file paths are relative, not absolute

4. **Slow Cold Starts**
   - Free tier apps sleep after inactivity
   - First request after sleep takes ~30 seconds
   - Consider paid plan for always-on service

### Alternative: Render from CLI

You can also deploy using Render CLI:

```bash
# Install Render CLI
npm install -g @render-tools/cli

# Login and deploy
render login
render deploy
```

## Comparison with Other Platforms

| Feature | Render | PythonAnywhere | Heroku |
|---------|--------|----------------|--------|
| Free Tier | 512MB, sleeps | 512MB, always on | No free tier |
| Build Time | Fast | Manual setup | Fast |
| Auto-deploy | Yes | Manual | Yes |
| Custom Domain | Paid plans | Paid plans | Paid plans |
| ML Libraries | Good support | Good support | Good support |

## Next Steps

1. Deploy your app following the steps above
2. Test the web interface
3. Upload or link your data files
4. Monitor performance and consider upgrading if needed

Your Deep Research Agent will be live and accessible to anyone with the URL!