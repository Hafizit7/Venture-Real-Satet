from django.db import models

# Create your models here.

class Admin(models.Model):
    admin_name = models.CharField(max_length=50,blank=True,null=True)
    admin_image = models.ImageField(upload_to="admin_images/",blank=True,null=True)
    dashboard_logo = models.ImageField(upload_to="admin_logos/",blank=True,null=True)

    def __str__(self):
        return self.admin_name

    class Meta:
        ordering = ['-id']