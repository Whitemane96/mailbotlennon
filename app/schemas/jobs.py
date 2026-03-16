from typing import Optional
from pydantic import BaseModel


class JobsListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    days: Optional[int] = None
    items: list[dict]


class JobsSummaryResponse(BaseModel):
    total_jobs_all_time: int
    total_jobs_recent: int
    sent_all_time: int
    sent_recent: int
    delivered_all_time: int
    delivered_recent: int
    needs_resend_all_time: int
    needs_resend_recent: int
    failed_all_time: int
    failed_recent: int
    cancelled_all_time: int
    cancelled_recent: int
    recent_days: int