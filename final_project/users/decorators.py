from django.shortcuts import redirect
def user_not_authenticated(function=None, redirect_url='/'):
    
    def decorator(view_func):
        def _wraped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wraped_view
    
    if function: #not none
        return decorator(function)
    
        
    return decorator