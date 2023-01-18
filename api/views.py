from telnetlib import STATUS
from urllib import response
from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from api.models import Todos
from api.serializer import TodoSerializer,RegistrationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions
from api.custom_permission import IsOwnerOrReadOnly
# Create your views here.

class TodoViews(ViewSet):
    def list(self,request,*args,**kw):
        qs=Todos.objects.all()
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def create(self,request,*args,**kw):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Todos.objects.get(id=id)
        serielizer=TodoSerializer(qs,many=True)
        return Response(data=serielizer.data)
    def destroy(self,request,*args,**kw):
        id=kw.get("pk")
        Todos.objects.get(id=id).delete()
        return Response(data="deleted")
    def update(self,request,*args,**kw):
        id=kw.get("pk")
        object=Todos.objects.get(id=id)
        serielizer=TodoSerializer(data=request.data,instance=object)
        if serielizer.is_valid():
            serielizer.save()
            return Response(data=serielizer.data)
        else:
            return Response(data=serielizer.errors)

class TodoModelViews(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[IsOwnerOrReadOnly]
    serializer_class=TodoSerializer
    queryset=Todos.objects.all()

    #TO CREATE TODOS BY SPECIFIC USERS(C)

    def create(self,request,*args,**kw):
        serializer=TodoSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    #TO CREATE TODOS BY SPECIFIC USERS(B)

    # def perform_create(self,serializer):
    #     serializer.save(user=self.request.user)

    #TO CREATE TODOS BY SPECIFIC USERS(A)

    # def create(self,request,*args,**kw):
    #     serializer=TodoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         Todos.objects.create(**serializer.validated_data,user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

    # TO LIST TODOS BY SPECIFIC USERS(A)

    # def list(self,request,*args,**kw):
    #     qs=Todos.objects.filter(user=request.user)
    #     serializer=TodoSerializer(qs,many=True)
    #     return Response(data=serializer.data)

    # TO LIST TODOS BY SPECIFIC USERS(B)

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)

    @action(methods=["GET"],detail=False)
    def pending_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=False,user=request.user)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["GET"],detail=False)
    def completed_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=True,user=request.user)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["PUT"],detail=True)
    def mark_as_read(self,request,*args,**kw):
        id=kw.get("pk")
        object=Todos.objects.get(id=id)
        object.status=True
        object.save()
        serializer=TodoSerializer(object,many=False)
        return Response(data=serializer.data)

class UserViews(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()

    # def create(self, request,*args,**kw):
    #     serializer=RegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         User.objects.create_user(**serializer.validated_data)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

