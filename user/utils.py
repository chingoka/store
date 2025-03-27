from venv import logger
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string
from django.shortcuts import redirect
from itsdangerous import URLSafeTimedSerializer # type: ignore
from store import settings
from user.models import User

def send_verification_email(email: str):
    try:
        user = User.get_user_by_email(email=email)
        if user is None:
            logger.error(f"User with email {email} not found.")
            return

        token = generate_verification_token(email)
        verification_url = f"{settings.FRONTEND_BASE_URL}verify-email?token={token}"

        subject = 'Verify Your Email'
        text_content = f"Hi {user.firstName} {user.lastName},\n\nPlease verify your email address by clicking the link below:\n{verification_url}\n\nThank you!"
        html_content = f"""
        <html>
            <body>
                <p>Hi {user.firstName} {user.lastName},</p>
                <p>Amazon Chingoka, we extend our sincerest gratitude for your agreement to work with you. We are delighted to welcome you to our community and look forward to providing you with  valuable resources, exclusive services, expert support and opportunity.</p>
                <p>Please verify your email address by clicking the button below:</p>
                <p>
                    <a href="{verification_url}" style="display: inline-block; padding: 10px 20px; font-size: 16px; color: #ffffff; background-color: #4CAF50; text-decoration: none; border-radius: 5px;">
                        Verify Email
                    </a>
                </p>
            </body>
        </html>
        """

        from_email = settings.DEFAULT_FROM_EMAIL
        email_to_user = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
        email_to_user.attach_alternative(html_content, "text/html")
        email_to_user.send()

    except Exception as e:
        logger.error(f"Error sending verification email to {email}: {str(e)}")
        raise Exception(f"Error sending email: {str(e)}")

    return redirect(f"{settings.FRONTEND_BASE_URL}/verify-email?token={token}")

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email)

def send_reset_email(email):
    try:
        user = User.objects.get(email=email)
        token = get_random_string(length=32)
        user.reset_token = token
        user.save()

        reset_url = f"{settings.FRONTEND_BASE_URL}/reset-password?token={token}"
        subject = "Password Reset Request"
        text_content = f"Hi {user.firstName} {user.lastName},\n\n "
        html_content = f"""
        <html>
            <body>
                <p>Hi {user.firstName} {user.lastName},</p>
                <p>Your email address has been sent for the purpose of reset password by clicking the link below:\n\n\nThank you!</p>
                <p>By clicking the button your  reset the password:</p>
                <p>
                    <a href="{reset_url}" style="display: inline-block; padding: 10px 20px; font-size: 16px; color: #ffffff; background-color: #4CAF50; text-decoration: none; border-radius: 5px;">
                        Reset Password
                    </a>
                </p>
            </body>
        </html>
        """

        from_email = settings.DEFAULT_FROM_EMAIL
        email_to_user = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
        email_to_user.attach_alternative(html_content, "text/html")
        email_to_user.send()

    except User.DoesNotExist:
        logger.error(f"User with email {email} does not exist.")
        raise Exception(f"User with email {email} does not exist.")
    except Exception as e:
        logger.error(f"Error sending password reset email to {email}: {str(e)}")
        raise Exception(f"Error sending email: {str(e)}")

    return redirect(f"{settings.FRONTEND_BASE_URL}/reset-password?token={token}")
