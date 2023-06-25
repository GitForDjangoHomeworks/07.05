from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

@login_required
@user_passes_test(lambda u: u.groups.filter(name='custom_group').exists() or u.is_superuser)
def is_user_authenticated(request):
    user = request.user
    print(f"User {user.username} is authenticated: {user.is_authenticated}")
    print(f"User {user.username} groups: {', '.join([group.name for group in user.groups.all()])}")

    return redirect('mainpage:show_mainpage')

