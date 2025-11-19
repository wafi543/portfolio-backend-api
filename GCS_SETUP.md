# Google Cloud Storage Setup Guide

## Overview
This guide helps you set up **Google Cloud Storage (GCS)** for image uploads with minimal costs (~$0-1/month for typical usage).

## GCP Free Tier Benefits
- **5GB free storage** per month
- **1GB free egress** per month
- **1 million free operations** per month

For a portfolio app, this is completely free!

---

## Step 1: Create GCP Project & Service Account

### 1.1 Create a new GCP Project
```bash
# In GCP Console, create a new project
# Project name: django-posts-api (or your preference)
# Take note of your Project ID
```

### 1.2 Enable Cloud Storage API
```bash
# In GCP Console:
# 1. Go to APIs & Services
# 2. Search for "Cloud Storage API"
# 3. Click Enable
```

### 1.3 Create Service Account
```bash
# In GCP Console:
# 1. Go to APIs & Services → Service Accounts
# 2. Click "Create Service Account"
# 3. Fill in:
#    - Service account name: django-app
#    - Service account ID: django-app
# 4. Click "Create and Continue"
# 5. Grant role: "Storage Object Admin"
# 6. Click "Continue" → "Done"
```

### 1.4 Create & Download Service Account Key
```bash
# In GCP Console:
# 1. Click on the service account you just created
# 2. Go to "Keys" tab
# 3. Click "Add Key" → "Create new key"
# 4. Choose "JSON" format
# 5. Click "Create"
# 6. The JSON file will download automatically
# 7. Save it securely (NEVER commit to git!)
```

---

## Step 2: Create GCS Bucket

### 2.1 Create the Bucket
```bash
# In GCP Console:
# 1. Go to Cloud Storage → Buckets
# 2. Click "Create Bucket"
# 3. Fill in:
#    - Name: portfolio-media-bucket (must be globally unique)
#    - Location: us-central1 (closest to your e2-micro)
#    - Storage class: Standard (optimized for frequent access and APIs)
#    - Access control: Uniform
# 4. Click "Create"
```

### 2.2 Set Public Access (for serving images)
```bash
# In GCP Console:
# 1. Open the bucket you created
# 2. Go to "Permissions" tab
# 3. Click "Grant Access"
# 4. Add: principal "allUsers" with role "Storage Object Viewer"
# 5. Click "Allow Public Access" (if prompted)

# Alternatively, enable public read via gsutil:
gsutil iam ch serviceAccount:django-app@PROJECT_ID.iam.gserviceaccount.com:objectViewer gs://portfolio-media-bucket
```

---

## Step 3: Configure Django

### 3.1 Set Environment Variables

Add to your `.env` file in `environments/.env`:

```bash
# Google Cloud Storage
GCS_PROJECT_ID=your-actual-project-id
GCS_BUCKET_NAME=portfolio-media-bucket
USE_GCS=True

# Set to 'prod' to enable GCS (or keep as 'local' for dev)
# CURRENT_ENV=prod
```

### 3.2 Set Up Service Account Credentials

**Option A: Using environment variable (Recommended for e2-micro)**
```bash
# In your e2-micro instance, set:
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# Add to your shell profile (~/.bashrc or ~/.zshrc) for persistence:
echo "export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json" >> ~/.bashrc
source ~/.bashrc
```

**Option B: In Docker (Recommended)**
```dockerfile
# In your Dockerfile, add:
COPY service-account-key.json /app/service-account-key.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json
```

### 3.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 3.4 Run Migrations
```bash
python manage.py makemigrations posts
python manage.py migrate
```

---

## Step 4: Test Upload

### Test via Django Shell
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from posts.models import Post
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

# Create a simple test image
img = Image.new('RGB', (100, 100), color='red')
img_io = BytesIO()
img.save(img_io, 'JPEG')
img_io.seek(0)

# Get or create user
user = User.objects.first()

# Create post with image
post = Post.objects.create(
    author=user,
    title='Test Post',
    body='Testing GCS upload',
    image=ContentFile(img_io.read(), name='test.jpg')
)

# Check if image URL is generated
print(post.image.url)
# Should output something like:
# https://storage.googleapis.com/portfolio-media-bucket/media/posts/2024/01/15/test.jpg
```

---

## Step 5: Test API Upload

### Using cURL
```bash
# Create a test image file
python3 << 'EOF'
from PIL import Image
Image.new('RGB', (200, 200), color='blue').save('test_image.jpg')
EOF

# Get JWT token first
TOKEN=$(curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_user","password":"your_pass"}' \
  | jq -r '.access')

# Upload post with image
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "title=Test Upload" \
  -F "body=Testing GCS" \
  -F "category=design" \
  -F "image=@test_image.jpg"
```

---

## Cost Breakdown (Standard Storage - Best for APIs)

### GCP Free Tier
| Item | Free Tier | Cost |
|------|-----------|------|
| Operations (1M/month) | ✓ | FREE |
| Egress (1GB/month) | ✓ | FREE |

### Standard Storage Pricing
| Item | Cost |
|------|------|
| Storage | $0.020/GB/month |
| Operations | Free (1M/month included) |
| Egress (after 1GB free) | $0.12/GB |

**For a portfolio with ~500 images (average 200KB each):**
- Storage: 100MB = $0.002/month
- Operations: ~1000 ops/month = Free (within 1M free)
- Egress: ~500MB = Free (within 1GB free)

**Monthly cost: ~$0.002 (essentially free!)**

### Why Standard is Best for Portfolios
- ✅ **Optimized for frequent access** (your API serving images)
- ✅ Better performance with no retrieval latency
- ✅ No minimum retention period
- ✅ 99.99% availability SLA (vs 99.9% for Nearline)
- ✅ Perfect for real-time API responses
- ✅ Still within free tier for typical usage

---

## Troubleshooting

### Issue: "DefaultCredentialsError" or "GOOGLE_APPLICATION_CREDENTIALS not set"
**Solution:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

### Issue: "Permission denied" when uploading
**Solution:**
1. Verify service account has "Storage Object Admin" role
2. Check bucket permissions allow the service account
3. Ensure bucket ACL allows writes

### Issue: Image URL returns 403 Forbidden
**Solution:**
1. Go to bucket permissions
2. Add "allUsers" with "Storage Object Viewer" role
3. Or make bucket public (less secure)

### Issue: Images not accessible from frontend
**Solution:**
1. Check CORS settings in settings.py
2. Verify MEDIA_URL is correct
3. Test URL directly in browser

---

## Security Best Practices

### 1. Don't commit service account key
```bash
# Add to .gitignore
echo "service-account-key.json" >> .gitignore
echo "environments/.env" >> .gitignore
```

### 2. Restrict bucket access
- Only grant necessary permissions to service account
- Use Workload Identity (if in GKE) instead of keys
- Rotate keys regularly

### 3. Enable versioning (optional)
```bash
gsutil versioning set on gs://portfolio-media-bucket
```

### 4. Set lifecycle rules (for cost optimization)
```bash
# Delete old objects after 90 days
gsutil lifecycle set - gs://portfolio-media-bucket <<< '
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {"age": 90}
      }
    ]
  }
}'
```

---

## Using gsutil Commands

```bash
# List all files in bucket
gsutil ls gs://portfolio-media-bucket/

# List files in media folder
gsutil ls gs://portfolio-media-bucket/media/

# Delete a specific file
gsutil rm gs://portfolio-media-bucket/media/posts/2024/01/15/old_image.jpg

# Monitor usage
gsutil du -s -h gs://portfolio-media-bucket/
```

---

## Local Development (Without GCS)

Keep `CURRENT_ENV=local` in settings.py to use local storage during development:

```bash
# Images will be saved to:
# ./media/posts/YYYY/MM/DD/filename.jpg

# Serve media files in development with django-extensions:
python manage.py runserver --nostatic
```

Then add to `urls.py`:
```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Migration from Local Storage

If you have existing images stored locally:

```bash
# Copy local media to GCS
gsutil -m cp -r ./media/* gs://portfolio-media-bucket/media/

# Or use django-storages management command
python manage.py collectstatic --no-input
```

---

## Next Steps

1. ✅ Create GCP project and service account
2. ✅ Create GCS bucket
3. ✅ Set environment variables
4. ✅ Run migrations
5. ✅ Test uploads
6. ✅ Deploy to e2-micro

Once deployed, all image uploads automatically go to GCS!
