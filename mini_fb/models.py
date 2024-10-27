from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
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
    
    def get_friends(self):
        # Retrieve all friends where this profile is either profile1 or profile2
        friends1 = Friend.objects.filter(profile1=self)
        friends2 = Friend.objects.filter(profile2=self)
        # Return a list of profiles, either from profile1 or profile2
        friends_list = [friend.profile2 for friend in friends1] + [friend.profile1 for friend in friends2]
        return friends_list
    def add_friend(self, other):
        """Adds a friend relationship between self and another profile, avoiding duplicates."""
        if self == other:
            raise ValueError("Cannot add yourself as a friend.")
        
        # Check for an existing friend relationship
        if not Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)
        ).exists():
            # No existing relationship, create a new one
            Friend.objects.create(profile1=self, profile2=other, timestamp=timezone.now())

    def get_friend_suggestions(self):
        """Returns Profiles who are not friends with self."""
        # Get all profiles except self and current friends
        friends = self.get_friends()
        return Profile.objects.exclude(pk=self.pk).exclude(pk__in=[friend.pk for friend in friends])
    
    def get_news_feed(self):
        # Get all friends of this profile
        friends = self.get_friends()

        # Get all status messages for this profile and its friends
        news_feed = StatusMessage.objects.filter(
            Q(profile=self) | Q(profile__in=friends)
        ).order_by('-timestamp')  # Order by the most recent first

        return news_feed

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
    
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name="profile2", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"friend: {self.profile1} & {self.profile2}"