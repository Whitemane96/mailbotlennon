from typing import Optional
from pydantic import BaseModel


class MondaySendFromDriveRequest(BaseModel):
    board_id: int
    item_id: int
    drive_folder_id: Optional[str] = None
    drive_file_id: Optional[str] = None
    expected_pdf_name: Optional[str] = None
    mailing_type: Optional[str] = None

    recipient_name: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[str] = None
    country: Optional[str] = "US"