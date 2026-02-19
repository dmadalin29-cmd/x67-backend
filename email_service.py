import resend
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "contact@x67digital.com")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "contact@x67digital.com")


class EmailService:
    @staticmethod
    async def send_contact_notification(contact_data: Dict[str, Any]) -> bool:
        """Send notification to admin about new contact"""
        try:
            params = {
                "from": FROM_EMAIL,
                "to": [ADMIN_EMAIL],
                "subject": f"🔔 Contact Nou: {contact_data['name']}",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%); padding: 30px; text-align: center;">
                        <h1 style="color: white; margin: 0;">Contact Nou Primit!</h1>
                    </div>
                    
                    <div style="padding: 30px; background: #f9fafb;">
                        <h2 style="color: #1f2937;">Detalii Contact:</h2>
                        
                        <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                            <p style="margin: 10px 0;"><strong>Nume:</strong> {contact_data['name']}</p>
                            <p style="margin: 10px 0;"><strong>Email:</strong> <a href="mailto:{contact_data['email']}">{contact_data['email']}</a></p>
                            <p style="margin: 10px 0;"><strong>Telefon:</strong> {contact_data.get('phone', 'Nu a furnizat')}</p>
                            <p style="margin: 10px 0;"><strong>Mesaj:</strong></p>
                            <div style="background: #f3f4f6; padding: 15px; border-radius: 6px; margin-top: 10px;">
                                {contact_data['message']}
                            </div>
                        </div>
                        
                        <p style="color: #6b7280; font-size: 14px; margin-top: 30px;">
                            Primit la: {contact_data.get('created_at', 'N/A')}
                        </p>
                    </div>
                </div>
                """
            }
            
            email = resend.Emails.send(params)
            return True
        except Exception as e:
            print(f"Error sending contact notification: {e}")
            return False

    @staticmethod
    async def send_contact_confirmation(contact_data: Dict[str, Any]) -> bool:
        """Send confirmation email to user"""
        try:
            params = {
                "from": FROM_EMAIL,
                "to": [contact_data['email']],
                "subject": "✅ Am primit mesajul tău - X67 Digital",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%); padding: 30px; text-align: center;">
                        <h1 style="color: white; margin: 0;">Mulțumim pentru mesaj!</h1>
                    </div>
                    
                    <div style="padding: 30px; background: #f9fafb;">
                        <p style="font-size: 16px; color: #1f2937;">Bună {contact_data['name']},</p>
                        
                        <p style="font-size: 16px; color: #1f2937; line-height: 1.6;">
                            Am primit mesajul tău și echipa noastră îl va revizui în cel mai scurt timp posibil. 
                            De obicei răspundem în maxim 24 de ore în zilele lucrătoare.
                        </p>
                        
                        <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                            <h3 style="color: #1f2937; margin-top: 0;">Mesajul tău:</h3>
                            <div style="background: #f3f4f6; padding: 15px; border-radius: 6px;">
                                {contact_data['message']}
                            </div>
                        </div>
                        
                        <p style="font-size: 16px; color: #1f2937; line-height: 1.6;">
                            În cazuri urgente, ne poți contacta direct la:
                        </p>
                        
                        <div style="background: white; padding: 15px; border-radius: 8px; margin: 20px 0;">
                            <p style="margin: 5px 0;">📞 <strong>Telefon:</strong> 0730 268 067</p>
                            <p style="margin: 5px 0;">📧 <strong>Email:</strong> contact@x67digital.com</p>
                        </div>
                        
                        <p style="font-size: 16px; color: #1f2937;">
                            Cu stimă,<br>
                            <strong>Echipa X67 Digital Media Groupe</strong>
                        </p>
                    </div>
                    
                    <div style="background: #1f2937; padding: 20px; text-align: center;">
                        <p style="color: #9ca3af; font-size: 12px; margin: 0;">
                            © 2026 X67 Digital Media Groupe. Toate drepturile rezervate.
                        </p>
                    </div>
                </div>
                """
            }
            
            email = resend.Emails.send(params)
            return True
        except Exception as e:
            print(f"Error sending confirmation email: {e}")
            return False

    @staticmethod
    async def send_newsletter_welcome(subscriber_data: Dict[str, Any]) -> bool:
        """Send welcome email to newsletter subscriber"""
        try:
            name = subscriber_data.get('name', 'Prieten')
            
            params = {
                "from": FROM_EMAIL,
                "to": [subscriber_data['email']],
                "subject": "🎉 Bine ai venit în comunitatea X67 Digital!",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%); padding: 30px; text-align: center;">
                        <h1 style="color: white; margin: 0;">Bine ai venit!</h1>
                    </div>
                    
                    <div style="padding: 30px; background: #f9fafb;">
                        <p style="font-size: 16px; color: #1f2937;">Salut {name}! 👋</p>
                        
                        <p style="font-size: 16px; color: #1f2937; line-height: 1.6;">
                            Mulțumim că te-ai abonat la newsletter-ul nostru! De acum vei primi:
                        </p>
                        
                        <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                            <ul style="list-style: none; padding: 0;">
                                <li style="padding: 10px 0; border-bottom: 1px solid #e5e7eb;">
                                    ✨ <strong>Ultimele tendințe</strong> în web design și development
                                </li>
                                <li style="padding: 10px 0; border-bottom: 1px solid #e5e7eb;">
                                    💡 <strong>Tips & Tricks</strong> pentru businessul tău online
                                </li>
                                <li style="padding: 10px 0; border-bottom: 1px solid #e5e7eb;">
                                    🎁 <strong>Oferte exclusive</strong> pentru abonați
                                </li>
                                <li style="padding: 10px 0;">
                                    📰 <strong>Noutăți</strong> despre proiectele noastre
                                </li>
                            </ul>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="https://x67digital.com" style="display: inline-block; background: linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold;">
                                Vizitează Website-ul
                            </a>
                        </div>
                        
                        <p style="font-size: 16px; color: #1f2937;">
                            Cu stimă,<br>
                            <strong>Echipa X67 Digital</strong>
                        </p>
                    </div>
                    
                    <div style="background: #1f2937; padding: 20px; text-align: center;">
                        <p style="color: #9ca3af; font-size: 12px; margin: 0;">
                            Vrei să te dezabonezi? <a href="#" style="color: #06B6D4;">Click aici</a>
                        </p>
                    </div>
                </div>
                """
            }
            
            email = resend.Emails.send(params)
            return True
        except Exception as e:
            print(f"Error sending welcome email: {e}")
            return False

    @staticmethod
    async def send_inquiry_notification(inquiry_data: Dict[str, Any]) -> bool:
        """Send template inquiry notification to admin"""
        try:
            params = {
                "from": FROM_EMAIL,
                "to": [ADMIN_EMAIL],
                "subject": f"🚀 Cerere Template Nouă: {inquiry_data['name']}",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #8B5CF6 0%, #06B6D4 100%); padding: 30px; text-align: center;">
                        <h1 style="color: white; margin: 0;">Cerere Template Nouă!</h1>
                    </div>
                    
                    <div style="padding: 30px; background: #f9fafb;">
                        <h2 style="color: #1f2937;">Detalii Cerere:</h2>
                        
                        <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                            <p style="margin: 10px 0;"><strong>Nume:</strong> {inquiry_data['name']}</p>
                            <p style="margin: 10px 0;"><strong>Email:</strong> <a href="mailto:{inquiry_data['email']}">{inquiry_data['email']}</a></p>
                            <p style="margin: 10px 0;"><strong>Telefon:</strong> {inquiry_data.get('phone', 'Nu a furnizat')}</p>
                            <p style="margin: 10px 0;"><strong>Tip Business:</strong> {inquiry_data['business_type']}</p>
                            <p style="margin: 10px 0;"><strong>Buget:</strong> {inquiry_data['budget']}</p>
                            <p style="margin: 10px 0;"><strong>Funcționalități:</strong> {inquiry_data['functionality']}</p>
                            <p style="margin: 10px 0;"><strong>Template ID:</strong> {inquiry_data.get('template_id', 'N/A')}</p>
                            {f'<p style="margin: 10px 0;"><strong>Note Adiționale:</strong><br>{inquiry_data.get("additional_notes", "")}</p>' if inquiry_data.get('additional_notes') else ''}
                        </div>
                    </div>
                </div>
                """
            }
            
            email = resend.Emails.send(params)
            return True
        except Exception as e:
            print(f"Error sending inquiry notification: {e}")
            return False

    @staticmethod
    async def send_inquiry_confirmation(inquiry_data: Dict[str, Any]) -> bool:
        """Send confirmation to user after template inquiry"""
        try:
            params = {
                "from": FROM_EMAIL,
                "to": [inquiry_data['email']],
                "subject": "✅ Cererea ta a fost primită - X67 Digital",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #8B5CF6 0%, #06B6D4 100%); padding: 30px; text-align: center;">
                        <h1 style="color: white; margin: 0;">Cererea ta a fost primită!</h1>
                    </div>
                    
                    <div style="padding: 30px; background: #f9fafb;">
                        <p style="font-size: 16px; color: #1f2937;">Bună {inquiry_data['name']},</p>
                        
                        <p style="font-size: 16px; color: #1f2937; line-height: 1.6;">
                            Mulțumim pentru interesul manifestat! Am primit cererea ta pentru un site web 
                            și echipa noastră o va analiza în detaliu.
                        </p>
                        
                        <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                            <h3 style="color: #1f2937; margin-top: 0;">Ce urmează?</h3>
                            <ol style="color: #4b5563; line-height: 1.8;">
                                <li>Analizăm cerințele tale</li>
                                <li>Pregătim o ofertă personalizată</li>
                                <li>Te contactăm în maxim 24h pentru detalii</li>
                            </ol>
                        </div>
                        
                        <p style="font-size: 16px; color: #1f2937;">
                            Cu stimă,<br>
                            <strong>Echipa X67 Digital</strong>
                        </p>
                    </div>
                </div>
                """
            }
            
            email = resend.Emails.send(params)
            return True
        except Exception as e:
            print(f"Error sending inquiry confirmation: {e}")
            return False
