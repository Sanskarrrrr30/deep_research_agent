# Memory Optimization Configuration

# For Render free tier (512MB RAM), use smaller models
RENDER_CONFIG = {
    'model_name': 'all-MiniLM-L12-v2',  # ~120MB vs all-MiniLM-L6-v2 ~400MB
    'chunk_size': 300,  # Smaller chunks to reduce memory usage
    'max_chunks': 50,   # Limit number of chunks processed at once
}

# For local development or paid hosting, use larger models
LOCAL_CONFIG = {
    'model_name': 'all-MiniLM-L6-v2',
    'chunk_size': 500,
    'max_chunks': 100,
}

# Auto-detect environment
import os
IS_RENDER = os.environ.get('RENDER') is not None
CONFIG = RENDER_CONFIG if IS_RENDER else LOCAL_CONFIG