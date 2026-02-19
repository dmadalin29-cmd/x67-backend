# X67 Digital Backend API

FastAPI backend with MongoDB and Resend email integration.

## Environment Variables Required

```env
MONGO_URL=your_mongodb_connection_string
DB_NAME=x67_digital_db
RESEND_API_KEY=re_haEunm2h_LxmJFHx89i2dp6Ubh6Aeqoyt
RESEND_FROM_EMAIL=contact@x67digital.com
ADMIN_EMAIL=contact@x67digital.com
JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=*
PORT=8001
```

## Railway Deployment

1. Create MongoDB database on Railway or MongoDB Atlas
2. Add all environment variables in Railway dashboard
3. Deploy from GitHub

## Endpoints

- `GET /api/` - API info
- `POST /api/contact` - Submit contact form
- `POST /api/newsletter/subscribe` - Subscribe to newsletter
- `POST /api/inquiries` - Submit template inquiry
- `GET /api/health` - Health check

## Local Development

```bash
pip install -r requirements.txt
python server.py
```
