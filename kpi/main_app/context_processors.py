from .models import Notification

# context processor that automatically provides the unread notification count to all templates, which allows the notification badge in the navbar to display across all pages without manually passing the count from every view function.
def notification_count(request):
    if request.user.is_authenticated and hasattr(request.user, 'employeeprofile'):
        if request.user.employeeprofile.role != 'admin':
            unread_count = Notification.objects.filter(
                recipient=request.user,
                is_read=False
            ).count()
            return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0}
