from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

User = get_user_model()

@require_POST
@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log the user out before deletion
    user.delete()    # This will trigger the post_delete signal
    return redirect('login')  # Redirect to login or homepage
