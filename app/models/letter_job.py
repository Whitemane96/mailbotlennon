from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class LetterJob(Base):
    __tablename__ = "letter_jobs"

    id = Column(Integer, primary_key=True, index=True)
    stannp_id = Column(String, index=True, nullable=True)
    stannp_status = Column(String(50), nullable=True, index=True)

    in_transit_scan_at = Column(DateTime, nullable=True)
    in_transit_location = Column(String(255), nullable=True)

    local_delivery_scan_at = Column(DateTime, nullable=True)
    local_delivery_location = Column(String(255), nullable=True)

    delivered_scan_at = Column(DateTime, nullable=True)
    delivered_location = Column(String(255), nullable=True)

    resend_count = Column(Integer, nullable=False, default=0)
    last_resend_at = Column(DateTime, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    recipient_name = Column(String, nullable=False)
    address1 = Column(String, nullable=False)
    address2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postcode = Column(String, nullable=False)
    country = Column(String, nullable=False, default="US")

    file_name = Column(String, nullable=True)
    pdf_path = Column(String, nullable=True)

    status = Column(String, nullable=False, default="sent")
    error_message = Column(Text, nullable=True)
    sent_at = Column(DateTime, default=datetime.utcnow)
    last_status_check = Column(DateTime, nullable=True)

    mailing_type = Column(String(100), index=True, nullable=True)

    user = relationship("User", back_populates="jobs")