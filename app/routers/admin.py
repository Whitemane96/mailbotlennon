from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.user import User
from app.schemas.auth import (
    UserOut,
    AdminInviteUserRequest,
    AdminCreatedUserResponse,
    AdminUpdateUserFlags,
    AdminResetPasswordResponse,
)
from app.services.auth_service import (
    require_admin,
    normalize_email,
    get_user_by_email,
    generate_temp_password,
    get_password_hash,
)

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/users", response_model=AdminCreatedUserResponse)
def admin_create_user(
    payload: AdminInviteUserRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    email_norm = normalize_email(payload.email)

    existing = get_user_by_email(db, email_norm)
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    temp_password = generate_temp_password()
    hashed_pw = get_password_hash(temp_password)

    user = User(
        email=email_norm,
        hashed_password=hashed_pw,
        role=payload.role,
        is_active=True,
        must_change_password=True,
        can_change_password=payload.can_change_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return AdminCreatedUserResponse(
        email=user.email,
        role=user.role,
        temp_password=temp_password,
        must_change_password=user.must_change_password,
        can_change_password=user.can_change_password,
    )


@router.get("/users", response_model=list[UserOut])
def admin_list_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    users = db.query(User).order_by(User.id.desc()).all()
    return users


@router.patch("/users/{user_id}", response_model=UserOut)
def admin_update_user(
    user_id: int,
    payload: AdminUpdateUserFlags,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.can_change_password is not None:
        user.can_change_password = payload.can_change_password
    if payload.is_active is not None:
        user.is_active = payload.is_active
    if payload.must_change_password is not None:
        user.must_change_password = payload.must_change_password
    if payload.role is not None:
        user.role = payload.role

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/users/{user_id}/reset_password", response_model=AdminResetPasswordResponse)
def admin_reset_password(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    temp_password = generate_temp_password()

    user.hashed_password = get_password_hash(temp_password)
    user.must_change_password = True
    user.can_change_password = True
    user.is_active = True

    db.add(user)
    db.commit()
    db.refresh(user)

    return AdminResetPasswordResponse(
        user_id=user.id,
        temp_password=temp_password,
    )


@router.delete("/users/{user_id}")
def admin_delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == current_admin.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot delete your own admin account.",
        )

    db.delete(user)
    db.commit()

    return {"status": "ok", "message": "User deleted."}