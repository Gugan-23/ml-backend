import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf import settings
import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User


# backend/views.py
# backend/views.py
# backend/views.py
from django.http import JsonResponse
from django.contrib.auth import get_user_model

def user_list(request):
    User = get_user_model()  # Retrieve the custom user model
    users = User.objects.all()  # Retrieve all user instances

    # Create a list of user data
    user_data = []
    for user in users:
        user_data.append({
            'name': user.username,
            'email': user.email,
            
        })

    return JsonResponse(user_data, safe=False)  # Return the user data as JSON

@csrf_exempt
def upload_appliance(request):
    if request.method == 'POST':
        appliance_type = request.POST.get('appliance_type')
        details = request.POST.get('details')
        photo = request.FILES.get('photo')

        # Ensure the upload directory exists
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Save the uploaded file
        if photo:
            file_path = os.path.join(upload_dir, photo.name)
            with open(file_path, 'wb+') as destination:
                for chunk in photo.chunks():
                    destination.write(chunk)

            return JsonResponse({'message': 'Upload successful', 'file_url': f'/media/uploads/{photo.name}'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

# backend/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def user_details(request):
    # Fetch the logged-in user's details
    user = request.user
    user_name = user.get_full_name()  # This will give the full name of the user
    user_email = user.email           # This will give the user's email

    # Pass the user details to the template
    return render(request, 'userdetails.html', {'user_name': user_name, 'user_email': user_email})

def list_uploaded_files(request):
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    try:
        # Initialize an empty list to hold file details
        file_details = []

        if os.path.exists(upload_dir):
            # List all files in the upload directory
            files = os.listdir(upload_dir)

            # Loop through each file to gather details
            for file in files:
                file_path = os.path.join(upload_dir, file)

                # Get file size in bytes
                file_size = os.path.getsize(file_path)

                # Get the last modified time
                last_modified_time = os.path.getmtime(file_path)
                last_modified = datetime.datetime.fromtimestamp(last_modified_time).strftime('%Y-%m-%d %H:%M:%S')

                # Create a dictionary for each file's details
                file_details.append({
                    'name': file,
                    'url': f'/media/uploads/{file}',
                    'size': file_size,  # Size in bytes
                    'last_modified': last_modified,
                })

        return JsonResponse({'uploaded_files': file_details})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)