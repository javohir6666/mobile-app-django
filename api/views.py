from django.shortcuts import render, redirect
from rest_framework import generics
from django.http import HttpResponseRedirect
from .models import Todo
from django.urls import reverse_lazy
from .serializers import TodoSerializer
from .forms import TodoForm
from django.views.generic.edit import UpdateView, DeleteView
from django.views import View
# Create your views here.

def index(request):
    page_title = 'Todo List'
    todos= Todo.objects.all()
    context = {
        'todos':todos,
        'page_title':page_title,
    }
    return render(request, 'index.html',context)
def create(request):
    form = TodoForm()
    page_title = 'Todo List'
    if request.method == "POST":
        #Get the posted form
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create")
    return render(request, "create.html", {"form": form,"page_title": page_title})

def isDone(request, pk):
    
    if request.method =='POST':
        print('alive')
        todo = Todo.objects.get(pk=pk)
        todo.isDone = True
        todo.save()

    return redirect('index')
        
   
class TodoGetCreate(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class TodoUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    
    
class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'delete.html'
    success_url = reverse_lazy('index')
    def test_func(self):
        todo = self.get_object()
        return self.request.user == todo.pk

class TodoEditView(UpdateView):
    model = Todo
    fields = ['title', 'desc']
    template_name = 'edit.html'
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('detail', kwargs = {'pk':pk})

    def test_func(self):
        todo = self.get_object()
        return self.request.user == todo.pk
    
class TodoDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        page_title = 'To do Detail'
        post = Todo.objects.get(pk=pk)
        form = TodoForm()
        
        context = {
            'todo': post,
            'form': form,
            'page_title':page_title,
        }

        return render(request, 'detail.html', context)