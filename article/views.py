from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import Content

# Create your views here.


class IndexView(ListView):

    model = Content
    template_name = 'index.html'
    context_object_name = 'post_list'
    paginate_by = 10




@login_required()
def home(request):
    if request.method == 'GET':

        return render(request, 'home.html', {'username':request.user.username})