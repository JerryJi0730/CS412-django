from django.db import models
class Profile(models.Model):
    '''Encapsulate the idea of an Article by some author.'''
    # data attributes of a Article:
    readonly_fields = ('id',)
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.EmailField(blank=False)
    profile_image_url=models.URLField(blank=False)
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.first_name} {self.last_name} comes from {self.city}. Email: {self.email_address}. Photo:{self.profile_image_url}'
    
    def get_status_messages(self):
        '''Retrieve all status messages for this Profile.'''
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')

class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now=True)  
    message = models.TextField(blank=False)  # The content of the status message
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        '''Return a string representation of this StatusMessage object.'''
        return f'Status from {self.profile}: "{self.message}" at {self.timestamp}'
# Create your models here.
