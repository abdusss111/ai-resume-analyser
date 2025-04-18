from rest_framework import permissions

class IsRecruiterOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'recruiter'

class IsRecruiterOrApplicant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'recruiter':
            return obj.job.recruiter == request.user
        return obj.applicant == request.user 