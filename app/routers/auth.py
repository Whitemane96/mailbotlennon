from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.user import User
from app.schemas.auth import (
    UserCreate,
    UserOut,
    LoginResponse,
    PasswordChangeRequest,
    EmailCheckResponse,
)
from app.services.auth_service import (
    normalize_email,
    get_user_by_email,
    get_password_hash,
    authenticate_user,
    create_access_token,
    verify_password,
    get_current_active_user,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    email_norm = normalize_email(payload.email)

    existing = get_user_by_email(db, email_norm)
    if existing:
        raise HTTPException(status_code=400, detail="Email is already registered.")

    hashed_pw = get_password_hash(payload.password)

    user = User(
        email=email_norm,
        hashed_password=hashed_pw,
        role="user",
        is_active=True,
        must_change_password=False,
        can_change_password=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password.",
        )

    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "must_change_password": user.must_change_password,
        "can_change_password": user.can_change_password,
        "role": user.role,
    }


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/check_email", response_model=EmailCheckResponse)
def check_email(email: str, db: Session = Depends(get_db)):
    email_norm = normalize_email(str(email))
    user = get_user_by_email(db, email_norm)
    if not user:
        return EmailCheckResponse(exists=False)

    return EmailCheckResponse(
        exists=True,
        must_change_password=user.must_change_password,
        role=user.role,
    )


@router.post("/change_password")
def change_password(
    payload: PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if not current_user.can_change_password:
        raise HTTPException(
            status_code=403,
            detail="Password changes are disabled for this account.",
        )

    if not verify_password(payload.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect.",
        )

    current_user.hashed_password = get_password_hash(payload.new_password)
    current_user.must_change_password = False

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {"status": "ok", "message": "Password updated successfully."}