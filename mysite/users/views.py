from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from .models import CustomUser

@login_required
def profile(request):
    profile_info = CustomUser.objects.get(username=request.user)

    return render(request, 'profile.html', {'profile_info': profile_info})



@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'change_profile.html'
    fields = ('first_name', 'last_name', 'bio',
              'location', 'birth_date', )
    success_url = reverse_lazy('users:profile')


    def get_object(self):
        return self.request.user
