from django.shortcuts import redirect

def login_required(view_func):
    """
    Restrict access to the dashboard to only authenticated users.
    If the user is not authenticated, redirect to login page.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

def unauthenticated_required(view_func):
    """
    Restrict access to the login view to only unauthenticated users.
    If the user is already authenticated, redirect them to the dashboard.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
