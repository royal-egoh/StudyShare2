from django.db import models
from django.contrib.auth.models import AbstractUser

FACULTY_DEPARTMENT_MAP = {
    'computing': {
        'computer_science': ['100', '200', '300', '400'],
        'software_engineering': ['100', '200', '300', '400'],
    },
    'engineering': {
        'mechanical_engineering': ['100', '200', '300', '400', '500'],
        'electrical_engineering': ['100', '200', '300', '400', '500'],
    },
    'arts': {
        'english': ['100', '200', '300', '400'],
        'music': ['100', '200', '300', '400'],
    }
}

LEVEL_CHOICES = [
    ('100', '100 Level'),
    ('200', '200 Level'),
    ('300', '300 Level'),
    ('400', '400 Level'),
    ('500', '500 Level'),
    ('600', '600 Level'),
]

FACULTY_CHOICES = [
    ('computing', 'Computing'),
    ('engineering', 'Engineering'),
    ('arts', 'Arts'),
]

DEPARTMENT_CHOICES = [
    ('computer_science', 'Computer Science'),
    ('software_engineering', 'Software Engineering'),
    ('mechanical_engineering', 'Mechanical Engineering'),
    ('electrical_engineering', 'Electrical Engineering'),
    ('english', 'English'),
    ('music', 'Music'),
]


class CustomUser(AbstractUser):
    faculty = models.CharField(max_length=100, choices=FACULTY_CHOICES)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES)
    
    def __str__(self):
        return f"{self.username} - {self.faculty} - {self.department} - {self.level}"