from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from accounts.models import CustomUser
from posts.models import Resource, RESOURCE_TYPE_CHOICES, SEMESTER_CHOICES
from django.db.models import Count
from django.contrib import messages

def get_semester():
    month = datetime.now().month
    if 9 <= month <= 12:
        return "first"
    return "second"

def update_level(user):
    now = datetime.now()
    max_level = 500 if user.faculty == 'engineering' else 400
    level = int(user.level)

    year = user.date_joined.year
    while True:
        year += 1
        if datetime(year, 9, 1) > now:
            break
        level += 100
        if level >= max_level:
            level = max_level
            break

    user.level = str(level)
    user.save()
    return user.level

@login_required(login_url='login')
def home(request):
    update_level(request.user)
    # print("SEMESTER:", get_semester())
    # print("LEVEL:", request.user.level, type(request.user.level))
    # print("TOTAL RESOURCES IN DB:", Resource.objects.count())
    resources = Resource.objects.filter(semester=get_semester(), level=request.user.level).order_by('-uploaded_at')
    print(f"COMBINED: {resources[0].raw_file.url}")
    return render(request, 'home.html', {'resources': resources, 'curr_semester': get_semester()})

@login_required(login_url='login')
def resource_details(request, resource_id):
    resource = Resource.objects.get(id=resource_id)
    return render(request, 'resource_detail.html', {'resource': resource})


@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        if ('file' not in request.FILES and request.POST.get('external_link') == ''):
            messages.error(request, "Please upload a file.")
            return redirect('upload')
        if request.POST.get('resource_type') == 'external_link':
            new_resource = Resource(semester= request.POST.get('semester'), title=request.POST.get('title'), description=request.POST.get('description'), resource_type=request.POST.get('resource_type'),
                                    external_link=request.POST.get('external_link'), 
            department=request.POST.get('department'), faculty=request.POST.get('faculty'), level=request.POST.get('level'), uploaded_by=request.user, uploaded_at=datetime.now())
        elif request.POST.get('resource_type') in ['video', 'audio']:
            new_resource = Resource(semester= request.POST.get('semester'), title=request.POST.get('title'), description=request.POST.get('description'), resource_type=request.POST.get('resource_type'),
                                    video_file=request.FILES.get('file'), 
            department=request.POST.get('department'), faculty=request.POST.get('faculty'), level=request.POST.get('level'), uploaded_by=request.user, uploaded_at=datetime.now())
        elif request.POST.get('resource_type') in ['lecture_notes', 'past_questions']:
            if request.FILES.get('file').name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                new_resource = Resource(semester= request.POST.get('semester'), title=request.POST.get('title'), description=request.POST.get('description'), resource_type=request.POST.get('resource_type'),
                                        image_file=request.FILES.get('file'), 
                department=request.POST.get('department'), faculty=request.POST.get('faculty'), level=request.POST.get('level'), uploaded_by=request.user, uploaded_at=datetime.now())
            else:
                new_resource = Resource(semester= request.POST.get('semester'), title=request.POST.get('title'), description=request.POST.get('description'), resource_type=request.POST.get('resource_type'),
                                        raw_file=request.FILES.get('file'), 
                department=request.POST.get('department'), faculty=request.POST.get('faculty'), level=request.POST.get('level'), uploaded_by=request.user, uploaded_at=datetime.now())
        else:
            new_resource = Resource(semester= request.POST.get('semester'), title=request.POST.get('title'), description=request.POST.get('description'), resource_type=request.POST.get('resource_type'),
                                    raw_file=request.FILES.get('file'), 
            department=request.POST.get('department'), faculty=request.POST.get('faculty'), level=request.POST.get('level'), uploaded_by=request.user, uploaded_at=datetime.now())
        new_resource.save()
        messages.success(request, "Resource uploaded successfully!")
        return redirect('resource_details', resource_id=new_resource.id)
    return render(request, 'upload.html')

@login_required(login_url='login')
def profile(request):
    resources = Resource.objects.filter(uploaded_by=request.user)
    most_common = (Resource.objects.values('resource_type').annotate(count=Count('resource_type')).order_by('-count').first())
    if most_common:
        most_uploaded_type = most_common['resource_type']
        for db_label, label in RESOURCE_TYPE_CHOICES:
            if most_uploaded_type == db_label:
                most_uploaded_type = label
    else:
        most_uploaded_type = "None"
    return render(request, 'profile.html', {'user': request.user, 'resources': resources, 'total_resources': len(resources), 'most_uploaded_type': most_uploaded_type})


@login_required(login_url='login')
def browse(request):
    resources = Resource.objects.all().order_by('-uploaded_at')
    return render(request, 'browse.html', {'resources': resources})


