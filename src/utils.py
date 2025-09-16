from fastapi import HTTPException


def check_permissions(current_user, user_id):
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Access denied, insufficient permissions")


def check_superuser_permission(current_user):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Access denied, insufficient permissions")