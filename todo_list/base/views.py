from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView , FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm  # built in form which will create new user for us after submitting form
from django.contrib.auth import login   #when user created we are automatically login that..without forcing login to that user and redirect to.
from .models import Task
 
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True 

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True 
    success_url = reverse_lazy('tasks')

    #now after registering or submitting the register page the user we are redirecting the user to given page.  once the form is submitting this form valid method is triggered
    def form_valid(self,form):
        user= form.save()  #after successfully creating the user we get the user in user variable
        if user is not None:
            login(self.request,user)   #user loggedin indirectly
        return super(RegisterPage,self).form_valid(form)   #and redirect the user ro list view

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(*args,**kwargs)


#if we want to restrict user to go on particular url or page if it is not authenticated then we use LoginRequireMixin.


# Create your views here.
class TaskList(LoginRequiredMixin, ListView):  #we are inheriting ListView and all those functionality ListView has now this class has also.
    model = Task
    context_object_name= 'tasks'

    def get_context_data(self, **kwargs):    #for the authenticate user corresponding tasks
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user) 
        context['count'] = context['tasks'].filter(complete=False).count() 
        search_input= self.request.GET.get('search-area') or '' #whatever user is input t the search-area it store in search-area variable of that form and then we are getting that data from this syntax and storing into search_input. 

        if search_input:
            #context['tasks'] = context['tasks'].filter(title__startswith=search_input)
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)   #any searches we are typing into searcharea we are filtering if it contains

        context['search_input'] =search_input  
        return context
    

class TaskDetail(LoginRequiredMixin,DetailView):   #this means if user want to go to any particular task he rquires login first.
    model =Task
    context_object_name= 'task'
    template_name= 'base/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model= Task 
    #fields= '__all__'
    fields = ['title','description','complete']
    success_url= reverse_lazy('tasks')  #if all thing right then redirect user to the url which has name tasks.

    def form_valid(self,form):   #jo user authenticate..for that user automatically task will create
        form.instance.user = self.request.user   #then post method request will done and then this method will triggered automatically at time of post request.
        return super(TaskCreate,self).form_valid(form)




class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    #fields= '__all__'
    fields = ['title','description','complete']
    success_url= reverse_lazy('tasks')

    

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task 
    context_object_name= 'task'
    success_url= reverse_lazy('tasks')
    #DeleteView bydefault search for task_confirm_delete.html  here task is model name





    
    
