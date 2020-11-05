from django.db import models

class Department(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='department_user')
    name = models.CharField(max_length=100, blank=True, null=True)
    join_id = models.CharField(max_length=32, blank=True, null=True)
    department_id = models.CharField(max_length=100, blank=True, null=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=32, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    organization = models.ForeignKey('organizations.Organization', blank=True, null=True, on_delete=models.SET_NULL, related_name='department_organization')
    requested_organization = models.ForeignKey('organizations.Organization', blank=True, null=True, on_delete=models.SET_NULL, related_name="department_requested_organization")
    accepting_req = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name