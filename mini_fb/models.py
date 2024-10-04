from django.db import models
class Profile(models.Model):
    '''Encapsulate the idea of an Article by some author.'''
    # data attributes of a Article:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.EmailField(blank=False)
    profile_image_url=models.URLField(blank=False)
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.first_name} {self.last_name} comes from {self.city}. Email: {self.email_address}. Photo:{self.profile_image_url}'
# Create your models here.
