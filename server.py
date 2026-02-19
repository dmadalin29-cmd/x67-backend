from fastapi import FastAPI, APIRouter, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import os
import logging

from models import (
    ContactCreate, Contact, ContactResponse,
    NewsletterSubscribe, Newsletter, NewsletterResponse,
    TemplateInquiryCreate, TemplateInquiry, InquiryResponse,
    MessageResponse, BlogPost, Project
)
from email_service import EmailService

# Setup
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL'].strip('"')
db_name = os.environ['DB_NAME'].strip('"')
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Initialize EmailService
email_service = EmailService()

# Create app
app = FastAPI(title="X67 Digital API", version="2.0")
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============= CONTACT ENDPOINTS =============

@api_router.post("/contact", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact_data: ContactCreate):
    """
    Create a new contact inquiry and send email notifications
    """
    try:
        # Create contact object
        contact = Contact(**contact_data.dict())
        
        # Save to database
        await db.contacts.insert_one(contact.dict())
        
        # Send email notifications (async fire-and-forget)
        try:
            await email_service.send_contact_notification(contact.dict())
            await email_service.send_contact_confirmation(contact.dict())
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            # Continue even if email fails
        
        return ContactResponse(
            message="Mesajul tău a fost trimis cu succes! Te vom contacta în curând.",
            success=True,
            contact_id=contact.id
        )
    
    except Exception as e:
        logger.error(f"Error creating contact: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A apărut o eroare. Te rugăm să încerci din nou."
        )


@api_router.get("/contacts")
async def get_contacts(limit: int = 50, skip: int = 0):
    """Get all contacts (Admin endpoint)"""
    try:
        contacts = await db.contacts.find().sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
        return {"contacts": contacts, "total": len(contacts)}
    except Exception as e:
        logger.error(f"Error fetching contacts: {e}")
        raise HTTPException(status_code=500, detail="Error fetching contacts")


# ============= NEWSLETTER ENDPOINTS =============

@api_router.post("/newsletter/subscribe", response_model=NewsletterResponse, status_code=status.HTTP_201_CREATED)
async def subscribe_newsletter(subscriber_data: NewsletterSubscribe):
    """
    Subscribe to newsletter
    """
    try:
        # Check if already subscribed
        existing = await db.newsletter.find_one({"email": subscriber_data.email})
        
        if existing:
            if existing.get('is_active'):
                return NewsletterResponse(
                    message="Ești deja abonat la newsletter!",
                    success=True
                )
            else:
                # Reactivate subscription
                await db.newsletter.update_one(
                    {"email": subscriber_data.email},
                    {"$set": {"is_active": True}}
                )
                return NewsletterResponse(
                    message="Abonamentul tău a fost reactivat cu succes!",
                    success=True
                )
        
        # Create new subscriber
        subscriber = Newsletter(**subscriber_data.dict())
        await db.newsletter.insert_one(subscriber.dict())
        
        # Send welcome email
        try:
            await email_service.send_newsletter_welcome(subscriber.dict())
        except Exception as e:
            logger.error(f"Welcome email failed: {e}")
        
        return NewsletterResponse(
            message="Te-ai abonat cu succes! Verifică-ți email-ul pentru confirmare.",
            success=True,
            subscriber_id=subscriber.id
        )
    
    except Exception as e:
        logger.error(f"Error subscribing to newsletter: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A apărut o eroare. Te rugăm să încerci din nou."
        )


@api_router.get("/newsletter/subscribers")
async def get_subscribers(limit: int = 100):
    """Get all newsletter subscribers (Admin endpoint)"""
    try:
        subscribers = await db.newsletter.find({"is_active": True}).sort("subscribed_at", -1).limit(limit).to_list(limit)
        return {"subscribers": subscribers, "total": len(subscribers)}
    except Exception as e:
        logger.error(f"Error fetching subscribers: {e}")
        raise HTTPException(status_code=500, detail="Error fetching subscribers")


# ============= TEMPLATE INQUIRY ENDPOINTS =============

@api_router.post("/inquiries", response_model=InquiryResponse, status_code=status.HTTP_201_CREATED)
async def create_inquiry(inquiry_data: TemplateInquiryCreate):
    """
    Create a new template inquiry
    """
    try:
        # Create inquiry object
        inquiry = TemplateInquiry(**inquiry_data.dict())
        
        # Save to database
        await db.inquiries.insert_one(inquiry.dict())
        
        # Send email notifications
        try:
            await email_service.send_inquiry_notification(inquiry.dict())
            await email_service.send_inquiry_confirmation(inquiry.dict())
        except Exception as e:
            logger.error(f"Inquiry email failed: {e}")
        
        return InquiryResponse(
            message="Cererea ta a fost înregistrată! Te vom contacta în curând cu o ofertă personalizată.",
            success=True,
            inquiry_id=inquiry.id
        )
    
    except Exception as e:
        logger.error(f"Error creating inquiry: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A apărut o eroare. Te rugăm să încerci din nou."
        )


@api_router.get("/inquiries")
async def get_inquiries(limit: int = 50):
    """Get all inquiries (Admin endpoint)"""
    try:
        inquiries = await db.inquiries.find().sort("created_at", -1).limit(limit).to_list(limit)
        return {"inquiries": inquiries, "total": len(inquiries)}
    except Exception as e:
        logger.error(f"Error fetching inquiries: {e}")
        raise HTTPException(status_code=500, detail="Error fetching inquiries")


# ============= BLOG ENDPOINTS =============

@api_router.get("/blog/posts")
async def get_blog_posts(limit: int = 10, skip: int = 0, category: str = None):
    """Get published blog posts"""
    try:
        query = {"published": True}
        if category:
            query["category"] = category
        
        posts = await db.blog_posts.find(query).sort("published_at", -1).skip(skip).limit(limit).to_list(limit)
        total = await db.blog_posts.count_documents(query)
        
        return {"posts": posts, "total": total}
    except Exception as e:
        logger.error(f"Error fetching blog posts: {e}")
        raise HTTPException(status_code=500, detail="Error fetching blog posts")


@api_router.get("/blog/posts/{slug}")
async def get_blog_post(slug: str):
    """Get single blog post by slug"""
    try:
        post = await db.blog_posts.find_one({"slug": slug, "published": True})
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching blog post: {e}")
        raise HTTPException(status_code=500, detail="Error fetching blog post")


# ============= PROJECT ENDPOINTS =============

@api_router.get("/projects")
async def get_projects(limit: int = 20, featured: bool = None, category: str = None):
    """Get projects"""
    try:
        query = {}
        if featured is not None:
            query["featured"] = featured
        if category:
            query["category"] = category
        
        projects = await db.projects.find(query).sort("completed_at", -1).limit(limit).to_list(limit)
        return {"projects": projects, "total": len(projects)}
    except Exception as e:
        logger.error(f"Error fetching projects: {e}")
        raise HTTPException(status_code=500, detail="Error fetching projects")


@api_router.get("/projects/{slug}")
async def get_project(slug: str):
    """Get single project by slug"""
    try:
        project = await db.projects.find_one({"slug": slug})
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching project: {e}")
        raise HTTPException(status_code=500, detail="Error fetching project")


# ============= STATS ENDPOINT =============

@api_router.get("/stats")
async def get_stats():
    """Get overall statistics"""
    try:
        total_contacts = await db.contacts.count_documents({})
        total_subscribers = await db.newsletter.count_documents({"is_active": True})
        total_inquiries = await db.inquiries.count_documents({})
        total_projects = await db.projects.count_documents({})
        
        return {
            "contacts": total_contacts,
            "newsletter_subscribers": total_subscribers,
            "template_inquiries": total_inquiries,
            "projects": total_projects
        }
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail="Error fetching stats")


# Root endpoint
@api_router.get("/")
async def root():
    return {
        "message": "X67 Digital API v2.0",
        "status": "operational",
        "endpoints": {
            "contact": "/api/contact",
            "newsletter": "/api/newsletter/subscribe",
            "inquiries": "/api/inquiries",
            "blog": "/api/blog/posts",
            "projects": "/api/projects",
            "stats": "/api/stats"
        }
    }


# Health check
@api_router.get("/health")
async def health_check():
    try:
        # Check MongoDB connection
        await db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


# Include router
app.include_router(api_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shutdown
@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
