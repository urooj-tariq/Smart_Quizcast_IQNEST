from django.shortcuts import render, redirect,get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import JsonResponse
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials
from .models import Rating
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test
from .models import MentorProfile


@login_required
def instructor_dashboard(request):
    mentor_profile = None
    if hasattr(request.user, 'mentor_profile'):
        mentor_profile = request.user.mentor_profile

    context = {
        'mentor_profile': mentor_profile
    }
    return render(request, 'instructor_dashboard.html', context)

@login_required
def student_dashboard(request):
    print("Student Dashboard - Current User:", request.user)  # Debugging
    print("Student Dashboard - Username:", request.user.username)  # Debugging

    context = {
        'username': request.user.username
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def instructor_dashboard(request):
    print("Instructor Dashboard - Current User:", request.user)  # Debugging
    print("Instructor Dashboard - Username:", request.user.username)  # Debugging

    context = {
        'username': request.user.username
    }
    return render(request, 'instructor_dashboard.html', context)




# Initialize Firebase Admin SDK
cred = credentials.Certificate(r'C:/Users/Tariq Ahmed/Downloads/smart-quizcast-firebase-adminsdk-l6qb6-357ee24891.json')

# Check if the app has already been initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Welcome page view
def welcome(request):
    return render(request, "quizcast/welcome.html")


#student_dashboard view:
def student_dashboard(request):
  
    return render(request, 'quizcast/student_dashboard.html')




 #student_dashboard   
@csrf_protect
def student_dashboard(request):

  

    if request.method == 'POST':
        # If the feedback button is clicked
        if request.POST.get('action') == 'feedback':
          return render(request, 'quizcast/rating.html')
          
        elif request.POST.get('action') == 'logout':
            return render(request, 'quizcast/welcome.html')

        elif request.POST.get('action') == 'Home':
           return render(request, 'quizcast/student_dashboard.html')
        
        elif request.POST.get('action') == 'Profile':
        

            return render(request, 'quizcast/profile.html')
        
        
          
          
    if request.user.is_authenticated and request.user.groups.filter(name='Students').exists():
        return render(request, 'quizcast/student_dashboard.html')
    else:
        return redirect('login')  # Redirect to login if not authenticatedsss
     
    
   
#logout view

def logout_view(request):
    if request.method=="POST":
        return redirect('welcome')


# User login view
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                
                # Check if the user is in the 'Students' group
                if user.groups.filter(name='Students').exists():
                    return redirect('student_dashboard')  
                
                elif user.groups.filter(name='Instructor').exists():
                    return redirect('instructor_dashboard')
                else:
                    return redirect('welcome')  
                
    else:
        form = AuthenticationForm()
    
    return render(request, 'quizcast/login.html', {'form': form})


#instructor_dashboard view:
def instructor_dashboard(request):
    

    if request.method == 'POST':

       if request.POST.get('action') == 'Logout':
            return render(request, 'quizcast/welcome.html')

    if request.user.is_authenticated and request.user.groups.filter(name='Instructor').exists():
        return render(request, 'quizcast/instructor_dashboard.html')
    

    
    else:
        return redirect('login')  
    

# rating views
def rating(request):
    if request.method == 'POST':
      return redirect(request, 'quizcast/rating.html')

@login_required
def profile_view(request):
    user = request.user  # Get the currently logged-in user
    
    if request.method == 'POST':
        # Update the user's information
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        
        user.save()  # Save the updated user info to the database
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')  # Redirect to the profile page after saving

    return render(request, 'quizcast/profile.html', {'user': user})
# Firestore 
db = firestore.client()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Add user to 'Students' group
            students_group, created = Group.objects.get_or_create(name='Students')
            students_group.user_set.add(user)

            # Firestore mein user details save karna
            try:
                db.collection('students').add({
                    'username': user.username,
                    'password': user.password,
                    'email': user.email,
                     'first_name': user.first_name,
                    'last_name': user.last_name,
                })
                print("Data successfully saved to Firestore.")
            except Exception as e:
                print(f"Error saving to Firestore: {e}")
            
            return redirect('login')
        else:
            print(form.errors)  # Debugging ke liye

    else:
        form = CustomUserCreationForm()

    return render(request, 'quizcast/register.html', {'form': form})


