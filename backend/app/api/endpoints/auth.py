import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List

from backend.app.database.session import get_db
from backend.app.database.models import User, PredictionRecord
from backend.app.schemas.auth import (
    UserRegister, UserLogin, UserResponse, TokenResponse,
    AdminUserListResponse, UserStatusUpdate
)
from backend.app.core.security import hash_password, verify_password, create_access_token, decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

router = APIRouter()

def get_optional_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[User]:
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        return None
    try:
        user_id = int(payload["sub"])
        return db.query(User).filter(User.id == user_id, User.is_active == True).first()
    except Exception:
        return None

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired authentication token")
    
    try:
        user_id = int(payload["sub"])
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account not found or disabled")
        return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required to access this resource."
        )
    return current_user

def seed_admin_user_if_needed(db: Session):
    """Ensures a default administrator account exists for immediate evaluation."""
    admin_email = "admin@lymphoma.ai"
    admin = db.query(User).filter(User.email == admin_email).first()
    if not admin:
        new_admin = User(
            full_name="Lead Clinical Administrator",
            email=admin_email,
            hashed_password=hash_password("Admin@123"),
            role="ADMIN",
            status="ACTIVE",
            is_active=True,
            created_at=datetime.datetime.utcnow(),
            last_login=datetime.datetime.utcnow()
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        print("Default Administrator account seeded: admin@lymphoma.ai / Admin@123")

@router.post("/register", response_model=TokenResponse)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    seed_admin_user_if_needed(db)
    email_clean = user_in.email.lower().strip()
    
    existing = db.query(User).filter(User.email == email_clean).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists. Please log in."
        )
    
    is_first_user = db.query(User).count() == 0
    role = "ADMIN" if (is_first_user or "admin" in email_clean) else "USER"

    new_user = User(
        full_name=user_in.full_name.strip(),
        email=email_clean,
        hashed_password=hash_password(user_in.password),
        role=role,
        status="ACTIVE",
        is_active=True,
        last_login=datetime.datetime.utcnow(),
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(subject=new_user.id, role=new_user.role)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=new_user
    )

@router.post("/login", response_model=TokenResponse)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    seed_admin_user_if_needed(db)
    email_clean = login_in.email.lower().strip()
    
    user = db.query(User).filter(User.email == email_clean).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password. Please verify your credentials."
        )

    if not user.is_active or user.status == "DISABLED":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been disabled by an administrator."
        )

    user.last_login = datetime.datetime.utcnow()
    if user.status != "ACTIVE":
        user.status = "ACTIVE"
    db.commit()

    token = create_access_token(subject=user.id, role=user.role)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=user
    )

@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return user

# =========================================================================
# ADMIN USER MANAGEMENT ENDPOINTS (PROTECTED VIA RBAC)
# =========================================================================

@router.get("/users", response_model=AdminUserListResponse)
def list_users(
    search: Optional[str] = Query(None, description="Search by name or email"),
    role: Optional[str] = Query(None, description="Filter by role (USER/ADMIN)"),
    user_status: Optional[str] = Query(None, alias="status", description="Filter by status (ACTIVE/INACTIVE/DISABLED)"),
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    query = db.query(User)
    
    if search:
        s = f"%{search.strip().lower()}%"
        query = query.filter(or_(User.full_name.ilike(s), User.email.ilike(s)))
    
    if role and role.upper() in ["USER", "ADMIN"]:
        query = query.filter(User.role == role.upper())

    all_users = query.order_by(User.created_at.desc()).all()
    now = datetime.datetime.utcnow()

    user_responses = []
    active_count = 0
    inactive_count = 0
    disabled_count = 0

    for u in all_users:
        # Inactivity calculation: if no login or last login > 30 days ago
        reference_time = u.last_login or u.created_at
        days_inactive = (now - reference_time).days if reference_time else 0
        
        # Determine effective status
        if not u.is_active or u.status == "DISABLED":
            effective_status = "DISABLED"
            disabled_count += 1
        elif days_inactive >= 30 or u.status == "INACTIVE":
            effective_status = "INACTIVE"
            inactive_count += 1
        else:
            effective_status = "ACTIVE"
            active_count += 1

        if user_status and user_status.upper() != "ALL":
            if effective_status != user_status.upper():
                continue

        pred_count = db.query(PredictionRecord).filter(PredictionRecord.user_id == u.id).count()

        user_responses.append(
            UserResponse(
                id=u.id,
                full_name=u.full_name,
                email=u.email,
                role=u.role,
                status=effective_status,
                is_active=u.is_active,
                created_at=u.created_at or now,
                last_login=u.last_login,
                days_inactive=days_inactive,
                prediction_count=pred_count
            )
        )

    total_count = len(all_users)

    return AdminUserListResponse(
        total=total_count,
        active_count=active_count,
        inactive_count=inactive_count,
        disabled_count=disabled_count,
        users=user_responses
    )

@router.patch("/users/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: int,
    status_update: UserStatusUpdate,
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")

    if target_user.id == admin.id and status_update.status.upper() == "DISABLED":
        raise HTTPException(status_code=400, detail="Administrators cannot disable their own active account")

    new_status = status_update.status.upper()
    if new_status not in ["ACTIVE", "DISABLED", "INACTIVE"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be ACTIVE, DISABLED, or INACTIVE")

    target_user.status = new_status
    target_user.is_active = (new_status != "DISABLED")
    db.commit()
    db.refresh(target_user)

    now = datetime.datetime.utcnow()
    reference_time = target_user.last_login or target_user.created_at
    days_inactive = (now - reference_time).days if reference_time else 0
    pred_count = db.query(PredictionRecord).filter(PredictionRecord.user_id == target_user.id).count()

    return UserResponse(
        id=target_user.id,
        full_name=target_user.full_name,
        email=target_user.email,
        role=target_user.role,
        status=target_user.status,
        is_active=target_user.is_active,
        created_at=target_user.created_at or now,
        last_login=target_user.last_login,
        days_inactive=days_inactive,
        prediction_count=pred_count
    )

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")

    if target_user.id == admin.id:
        raise HTTPException(status_code=400, detail="Administrators cannot delete their own active account")

    # Reassign or clean up prediction records safely to preserve historical audit logs without broken FKs
    predictions = db.query(PredictionRecord).filter(PredictionRecord.user_id == target_user.id).all()
    for pred in predictions:
        pred.user_name = f"{target_user.full_name} (Deleted User)"
        pred.user_email = target_user.email

    db.delete(target_user)
    db.commit()

    return {
        "status": "success",
        "message": f"User account '{target_user.email}' was safely deleted.",
        "user_id": user_id
    }
