from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def things(request):
    """example api route"""

    response = JsonResponse({'stuff':'things'})
    return response
