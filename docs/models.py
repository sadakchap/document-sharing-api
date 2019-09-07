from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Doc(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_docs')
    f       = models.FileField(upload_to='user_files/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self._file.name} uploaded by {self.user.email} '
    
    class Meta:
        ordering = ('-created',)
