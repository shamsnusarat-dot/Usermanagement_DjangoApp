from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from .models import User
from .serializers import UserSerializer

class UserListCreateView(APIView):
    def get(self, request):
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get(self, request, pk):
        return Response(UserSerializer(get_object_or_404(User, pk=pk)).data)

    def put(self, request, pk):
        serializer = UserSerializer(get_object_or_404(User, pk=pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        serializer = UserSerializer(get_object_or_404(User, pk=pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        get_object_or_404(User, pk=pk).delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class UserListTemplateView(View):
    def get(self, request):
        return render(request, 'users/user_list.html', {'users': User.objects.all()})


class UserCreateTemplateView(View):
    def get(self, request):
        return render(request, 'users/user_form.html')

    def post(self, request):
        data = request.POST
        serializer = UserSerializer(data={'name': data.get('name'), 'email': data.get('email'), 'phone': data.get('phone', '')})
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'User created successfully.')
            return redirect('user-list-template')
        return render(request, 'users/user_form.html', {'errors': serializer.errors})


class UserEditTemplateView(View):
    def get(self, request, pk):
        return render(request, 'users/user_form.html', {'user': get_object_or_404(User, pk=pk)})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        data = request.POST
        serializer = UserSerializer(user, data={'name': data.get('name'), 'email': data.get('email'), 'phone': data.get('phone', '')})
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'User updated successfully.')
            return redirect('user-list-template')
        return render(request, 'users/user_form.html', {'user': user, 'errors': serializer.errors})


class UserDeleteTemplateView(View):
    def get(self, request, pk):
        return render(request, 'users/user_confirm_delete.html', {'user': get_object_or_404(User, pk=pk)})

    def post(self, request, pk):
        get_object_or_404(User, pk=pk).delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('user-list-template')
