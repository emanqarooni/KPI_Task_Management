from .models import ActivityLog

def log_activity(user, action, description, related_user=None):
    """
    Simple function to log user activities

    Args:
        user: The user performing the action
        action: Action type from ActivityLog.ACTION_CHOICES
        description: Human-readable description of what happened
        related_user: Optional - the employee/user affected by the action
    """
    ActivityLog.objects.create(
        user=user,
        action=action,
        description=description,
        related_user=related_user
    )
