import asyncio
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum

from app.core import settings

logger = logging.getLogger(__name__)

_EXCLUDED_FIELDS = {"id", "created_at", "updated_at"}

_LABEL_MAP = {
    "full_name": "Full Name",
    "mobile_number": "Mobile Number",
    "email": "Email Address",
    "whatsapp_number": "WhatsApp Number",
    "qualification": "Qualification",
    "workshop_name": "Workshop Name",
    "workshop_type": "Workshop Type",
    "project_details": "Project Details",
    "file_url": "File URL",
    "material": "Material",
    "length_x": "Length (X)",
    "width_y": "Width (Y)",
    "height_z": "Height (Z)",
    "image_urls": "Image URLs",
    "product_images": "Product Images",
}

_IMAGE_FIELDS = {"file_url", "image_urls", "product_images"}

_IMG_TAG = '<img src="{url}" alt="Uploaded Image" style="max-width:100%;height:auto;border-radius:8px;margin-top:4px;" />'


def _format_value(key: str, value) -> str:
    """Convert field values to HTML-safe strings, rendering images for known image fields."""
    if isinstance(value, Enum):
        return value.value.replace("_", " ").title()
    if key in _IMAGE_FIELDS:
        urls = value if isinstance(value, list) else [value]
        return "".join(_IMG_TAG.format(url=u) for u in urls)
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


def _build_html(module_name: str, data: dict) -> str:
    rows = "".join(
        f"""
        <tr>
            <td style="padding:6px 12px;font-weight:600;white-space:nowrap;vertical-align:top;color:#333;">{_LABEL_MAP.get(key, key.replace('_', ' ').title())}</td>
            <td style="padding:6px 4px;color:#555;">:</td>
            <td style="padding:6px 12px;color:#333;">{_format_value(key, value)}</td>
        </tr>"""
        for key, value in data.items()
        if key not in _EXCLUDED_FIELDS and value is not None
    )

    return f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;border:1px solid #e0e0e0;border-radius:8px;overflow:hidden;">
        <div style="background:#1a1a2e;padding:20px 24px;display:flex;align-items:center;gap:12px;">
            <img src="https://veomalabs.com/logo.png" alt="VEOMA Labs Logo" width="120" style="display:block;" />
            <h2 style="color:#ffffff;margin:0;font-size:18px;">{module_name}</h2>
        </div>
        <div style="padding:24px;">
            <p style="color:#444;margin-top:0;">Dear Team,</p>
            <p style="color:#444;">A new submission has been received from <strong>Veoma Labs</strong>. Please find the details below:</p>
            <table style="border-collapse:collapse;width:100%;margin-top:12px;">
                {rows}
            </table>
            <hr style="margin:24px 0;border:none;border-top:1px solid #eee;">
            <p style="color:#888;font-size:13px;margin:0;">Regards,<br><strong>VEOMA Labs System</strong></p>
        </div>
    </div>
    """


def _send_sync(subject: str, html_body: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USER
    msg["To"] = settings.EMAIL_RECEIVER
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, settings.EMAIL_RECEIVER, msg.as_string())


async def send_submission_email(module_name: str, data: dict) -> None:
    """Send a formatted HTML submission notification email.

    Args:
        module_name: Display name of the module (e.g. "Workshop Registration").
        data: Submitted payload as a dict (model_dump output).
    """
    subject = "New Submission Received from Veoma Labs"
    body = _build_html(module_name, data)
    try:
        await asyncio.to_thread(_send_sync, subject, body)
        logger.info("Email sent for: %s", module_name)
    except Exception:
        logger.exception("Failed to send email for: %s", module_name)
