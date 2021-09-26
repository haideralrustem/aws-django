from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, default='')

    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
        
            img.save(self.image.path)
    
    def get_image(self):
        if self.pk is not None:
            orig = Profile.objects.get(pk=self.pk)
            if orig.image != self.image:
                print (' \n\n\n image changed \n\n\n')
                return True
            else:
                
                print ('\n\n\n image Has not changed changed \n\n\n')
                return False
