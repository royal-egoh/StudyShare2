from django.db import models
from accounts.models import CustomUser, DEPARTMENT_CHOICES, FACULTY_CHOICES, LEVEL_CHOICES
from cloudinary_storage.storage import RawMediaCloudinaryStorage, VideoMediaCloudinaryStorage, MediaCloudinaryStorage
from cloudinary_storage.validators import validate_video
import uuid

RESOURCE_TYPE_CHOICES = [
    ('lecture_notes', 'Lecture Notes'),
    ('past_questions', 'Past Questions'),
    ('audio_file', 'Audio File'),
    ('video', 'Video'),
    ('external_link', 'External Link'),
]

# FILE_TYPE_CHOICES = [
#     ('pdf', 'PDF'),
#     ('image', 'Image'),
#     ('word', 'Word Document'),
#     ('video', 'Video'),
#     ('text', 'Text'),
#     ('link', 'Link'),
#     ('other', 'Other'),
# ]

SEMESTER_CHOICES = [
    ('first', 'First Semester'),
    ('second', 'Second Semester'),
]

class Resource(models.Model):
    semester = models.CharField(max_length=100, choices=SEMESTER_CHOICES, default='first')
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, blank=True, null=True)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPE_CHOICES)
    
    image_file = models.ImageField(upload_to='image_resources/', blank=True, null=True, storage=MediaCloudinaryStorage())
    raw_file = models.FileField(upload_to='raw_resources/', blank=True, null=True, storage=RawMediaCloudinaryStorage())
    video_file = models.ImageField(upload_to='video_resources/', blank=True, null=True, storage=VideoMediaCloudinaryStorage(), validators=[validate_video])
    
    external_link = models.URLField(blank=True, null=True)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    faculty = models.CharField(max_length=100, choices=FACULTY_CHOICES)
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES)
    
    uploaded_by = models.ForeignKey(to=CustomUser, on_delete=models.SET_DEFAULT, default='Deleted User', related_name='resources')
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    download_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.title} — {self.faculty} — {self.department} — {self.level}"
    
    
