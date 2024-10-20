from django.db import models
from django.urls import reverse
from django.utils import timezone
class Profile(models.Model):
    '''Encapsulate the idea of an Article by some author.'''
    # data attributes of a Article:
    readonly_fields = ('id',)
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.EmailField(blank=False)
    profile_image_url=models.URLField(blank=False,default='http://example.com/default-image.jpg')
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.first_name} {self.last_name} comes from {self.city}. Email: {self.email_address}. Photo:{self.profile_image_url}'
    
    def get_status_messages(self):
        '''Retrieve all status messages for this Profile.'''
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    def get_absolute_url(self):
        '''Return the URL to access a detail record for this profile.'''
        return reverse('show_profile', kwargs={'pk': self.pk})

class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now=True)  
    message = models.TextField(blank=False)  # The content of the status message
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        '''Return a string representation of this StatusMessage object.'''
        return f'Status from {self.profile}: "{self.message}" at {self.timestamp}'
    def get_absolute_url(self):
        '''Return the URL to access a detail record for this profile.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_images(self):
        '''Return all images associated with this status message.'''
        return Image.objects.filter(status_message=self).order_by('-timestamp')
    

class Image(models.Model):
    '''Represents an image associated with a status message.'''
    image_file = models.ImageField(upload_to='images/')  # Storing the image file
    timestamp = models.DateTimeField(default=timezone.now)  # When the image was uploaded
    status_message = models.ForeignKey('StatusMessage', on_delete=models.CASCADE)  # FK to StatusMessage

    def __str__(self):
        return f"Image uploaded at {self.timestamp} for {self.status_message}"