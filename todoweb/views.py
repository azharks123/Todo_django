from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView,CreateView,FormView,ListView,DetailView
from django.contrib.auth.models import User
from api.models import Todos
from django.contrib.auth import authenticate,login,logout
from todoweb.forms import UserRegisterationForm,LoginForm,TodosForm
from django.utils.decorators import method_decorator
from django.contrib import messages

# Create your views here.

def signin_requerment(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"You must log in first")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper

class RegisterView(CreateView):
    template_name="register.html"
    form_class=UserRegisterationForm
    model=User
    success_url=reverse_lazy("signin")





    # def get(self,request,*args,**kw):
    #     form=UserRegisterationForm()
    #     return render(request,"register.html",{"form":form})
    
    # def post(self,request,*args,**kw):
    #     form=UserRegisterationForm(request.POST)
    #     if form.is_valid():
    #         User.objects.create_user(**form.cleaned_data)
    #         messages.success(request,"Successfully created")
    #         return redirect("signin")
    #     else:
    #         return render(request,"register.html",{"form":form})

class LoginView(FormView):
    template_name="login.html"
    form_class=LoginForm
    # def get(self,request,*args,**kw):
    #     form=LoginForm()
    #     return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)

        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(uname,pwd)
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"Login successfull")
                return redirect("home")
            else:
                print("invalid")
                return render(request,"login.html",{"form":form})

@method_decorator(signin_requerment,name="dispatch")
class IndexView(TemplateView):
    template_name="index.html"

@method_decorator(signin_requerment,name="dispatch")
class TodoListView(ListView):
    template_name="todo-list.html"
    model=Todos
    context_object_name="todos"

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)

    # def get(self,request,*args,**kw):
    #     qs=Todos.objects.filter(user=request.user)
    #     return render(request,"todo-list.html",{"todos":qs})

@method_decorator(signin_requerment,name="dispatch")
class TodoCreateView(CreateView):
    template_name="todo-add.html"
    form_class=TodosForm
    model=Todos
    success_url=reverse_lazy("todo-list")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"Created Successfully")
        return super().form_valid(form)

    # def get(self,request,*args,**kw):
    #     form=TodosForm()
    #     return render(request,"todo-add.html",{"form":form})
    # def post(self,request,*args,**kw):
    #     form=TodosForm(request.POST)
    #     if form.is_valid():
    #         instance=form.save(commit=False)
    #         instance.user=request.user
    #         instance.save()
    #         messages.success(request,"created successfully")
    #         return redirect("todo-add")
    #     else:
    #         return render(request,"todo-add.html",{"form":form})

@method_decorator(signin_requerment,name="dispatch")
class TodoDetailView(DetailView):
    template_name="todo-detail.html"
    model=Todos
    context_object_name="todos"
    pk_url_kwarg="id"
    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     qs=Todos.objects.get(id=id)
    #     return render(request,"todo-detail.html",{"todos":qs})

@signin_requerment
def todo_delete_view(request,*args,**kw):
    id=kw.get("id")
    Todos.objects.get(id=id).delete()
    messages.success(request,"Removed successfully")
    return redirect("todo-list")

def sign_out_view(request,*args,**kw):
    logout(request)
    return redirect("signin")