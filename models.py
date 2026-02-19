from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
import uuid


# Contact Form Models
class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    message: str = Field(..., min_length=10, max_length=2000)


class Contact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    phone: Optional[str] = None
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "new"  # new, read, replied


# Newsletter Models
class NewsletterSubscribe(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class Newsletter(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    name: Optional[str] = None
    subscribed_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True


# Template Inquiry Models
class TemplateInquiryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    business_type: str
    budget: str
    functionality: str
    template_id: Optional[str] = None
    additional_notes: Optional[str] = Field(None, max_length=1000)


class TemplateInquiry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    phone: Optional[str] = None
    business_type: str
    budget: str
    functionality: str
    template_id: Optional[str] = None
    additional_notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"  # pending, contacted, converted, rejected


# Blog Models
class BlogPost(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    slug: str
    excerpt: str
    content: str
    author: str
    category: str
    tags: List[str] = []
    featured_image: Optional[str] = None
    published: bool = False
    published_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Project Models
class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    slug: str
    description: str
    client: str
    category: str
    tags: List[str] = []
    featured_image: str
    images: List[str] = []
    url: Optional[str] = None
    completed_at: Optional[datetime] = None
    featured: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Response Models
class MessageResponse(BaseModel):
    message: str
    success: bool = True


class ContactResponse(MessageResponse):
    contact_id: Optional[str] = None


class NewsletterResponse(MessageResponse):
    subscriber_id: Optional[str] = None


class InquiryResponse(MessageResponse):
    inquiry_id: Optional[str] = None
