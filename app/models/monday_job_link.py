from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.db import Base


class MondayJobLink(Base):
    __tablename__ = "monday_job_links"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("letter_jobs.id"), nullable=False, index=True)

    monday_board_id = Column(String, nullable=False, index=True)
    monday_item_id = Column(String, nullable=False, index=True)

    drive_folder_id = Column(String, nullable=True)
    drive_file_id = Column(String, nullable=True)
    expected_file_name = Column(String, nullable=True)

    source_action = Column(String, nullable=True)
    last_monday_sync_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)