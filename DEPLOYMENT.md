# Vercel Deployment Guide

## Database Setup

Since Vercel is serverless, you need a cloud database. Options:

### 1. PlanetScale (Recommended)
1. Sign up at [planetscale.com](https://planetscale.com)
2. Create a new database
3. Get connection details from dashboard
4. Add environment variables in Vercel

### 2. Railway
1. Sign up at [railway.app](https://railway.app)
2. Create MySQL database
3. Get connection string
4. Add to Vercel environment variables

### 3. Aiven
1. Sign up at [aiven.io](https://aiven.io)
2. Create MySQL service
3. Get connection details
4. Add to Vercel environment variables

## Vercel Environment Variables

Add these in your Vercel project settings:

```
DB_HOST=your_database_host
DB_USER=your_database_user  
DB_PASSWORD=your_database_password
DB_NAME=movie_booking_system
DB_PORT=3306
```

## Deploy Steps

1. Push code to GitHub
2. Connect repository to Vercel
3. Add environment variables
4. Deploy

## Initialize Database

After deployment, visit `/init-db` endpoint to create tables and sample data.

## Local Development

1. Copy `.env.example` to `.env`
2. Update with your local MySQL credentials
3. Run `python app.py`