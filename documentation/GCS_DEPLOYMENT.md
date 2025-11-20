# GCS Deployment Guide - Europe-West1

## Setup Completion Checklist

### ✅ Configuration Files Updated
- [x] `config/settings.py` - GCS configuration for europe-west1
- [x] `posts/models.py` - Uses GoogleCloudStorage backend
- [x] `posts/serializers.py` - Image validation (5MB limit)
- [x] `posts/views.py` - Image upload endpoint ready

### Step 1: Add Service Account Key to Environment

1. **Download your service account JSON key from GCP Console**
   - Go to: IAM & Admin → Service Accounts
   - Click your service account
   - Keys tab → Create new key → JSON format

2. **Set the environment variable (choose one method)**

   **Option A: Local Development**
   ```bash
   # Add to environments/.env
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
   ```

   **Option B: Docker/Production**
   - Store the JSON key in a secure location (e.g., Google Secret Manager)
   - Set `GOOGLE_APPLICATION_CREDENTIALS` to point to the mounted file

### Step 2: Enable GCS in environment/.env

```bash
# Uncomment and set these values in environments/.env:
export USE_GCS="True"
export GCS_PROJECT_ID="your-actual-gcp-project-id"
export GCS_BUCKET_NAME="your-bucket-name"
export GCS_REGION="europe-west1"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

### Step 3: Verify GCS Bucket Configuration

Your bucket should have these settings:
- **Location**: europe-west1
- **Storage Class**: Standard
- **Access Control**: Uniform
- **Public Access**: Allowed (for serving images)

### Step 4: Test Image Upload Endpoint

**Create a Post with Image:**
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "title=My Portfolio Piece" \
  -F "subtitle=An amazing design" \
  -F "category=design" \
  -F "body=This is my portfolio project" \
  -F "image=@/path/to/image.jpg"
```

**Response Example:**
```json
{
  "id": 1,
  "title": "My Portfolio Piece",
  "subtitle": "An amazing design",
  "image": "https://storage.googleapis.com/your-bucket-name/media/posts/2025/11/20/image.jpg",
  "category": "design",
  "body": "This is my portfolio project",
  "author": {
    "id": 1,
    "username": "your_username",
    "email": "your@email.com"
  },
  "created_at": "2025-11-20T12:00:00Z",
  "updated_at": "2025-11-20T12:00:00Z"
}
```

## API Endpoints

### Create Post with Image
- **Endpoint**: `POST /api/posts/`
- **Authentication**: Required (JWT Bearer token)
- **Content-Type**: `multipart/form-data`

**Form Parameters:**
| Parameter | Type | Required | Notes |
|-----------|------|----------|-------|
| title | string | ✓ | Max 200 characters |
| subtitle | string | ✗ | Max 300 characters |
| body | string | ✓ | Post content |
| image | file | ✗ | Max 5MB, JPEG/PNG |
| category | string | ✓ | One of: photography, video, branding, design |

### Update Post with Image
- **Endpoint**: `PATCH /api/posts/{id}/`
- **Authentication**: Required (JWT Bearer token)
- **Content-Type**: `multipart/form-data`

### Retrieve Post
- **Endpoint**: `GET /api/posts/{id}/`
- **Authentication**: Required (owner only)

### List User's Posts
- **Endpoint**: `GET /api/posts/`
- **Authentication**: Required
- **Query Parameters**: 
  - `recent=true` - Get last 6 recent posts

## Image Storage Details

- **Upload Path**: `posts/YYYY/MM/DD/filename.jpg`
- **Public URL**: `https://storage.googleapis.com/bucket-name/media/posts/YYYY/MM/DD/filename.jpg`
- **Max File Size**: 5MB
- **Allowed Formats**: JPEG, PNG, WebP, and other Django-supported formats
- **Access**: Public read, authenticated write

## GCS Cost Optimization

For your portfolio app, this setup is **nearly free**:
- **Free Tier**: 5GB storage/month, 1GB egress/month, 1M operations/month
- **Typical Portfolio Usage**: ~100MB storage, minimal egress
- **Estimated Cost**: $0-1/month

## Troubleshooting

### Error: "GOOGLE_APPLICATION_CREDENTIALS not found"
- Ensure service account JSON key path is correct
- Key must be readable by Django process
- Check file permissions: `chmod 600 /path/to/key.json`

### Error: "Bucket not found"
- Verify bucket name matches exactly (case-sensitive)
- Confirm bucket exists in GCP Console
- Check service account has "Storage Object Admin" role

### Error: "403 Forbidden - Access Denied"
- Service account needs "Storage Object Admin" role
- Bucket must have public access enabled for serving images
- Check bucket's IAM permissions in GCP Console

### Images not accessible after upload
- Verify `GS_DEFAULT_ACL = 'public-read'` in settings
- Check bucket's "Uniform" access control is enabled
- Ensure `GS_QUERYSET_AUTH = False` in settings

## Next Steps

1. ✅ Environment variables configured
2. ✅ Django settings updated
3. ⬜ Service account key added to server
4. ⬜ Test upload via API
5. ⬜ Deploy to production

For production deployment, consider:
- Using Google Secret Manager for credentials
- Setting up CDN (Cloud CDN) for faster image delivery
- Implementing image optimization/resizing
- Adding backup/disaster recovery strategy
