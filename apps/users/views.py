# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages


def index(req):
  if 'user_id' not in req.session:
    return redirect('users:new')

  user_id = req.session['user_id']
  context = {
    'user': User.objects.get(id=user_id),
    'all': User.objects.all()
  }
  return render(req, 'users/index.html', context)

def new(req):
  return render(req, 'users/new.html')

def create(req):
  if req.method != 'POST':
    return redirect('users:new')

  valid, result = User.objects.validate_and_create_user(req.POST)
  if not valid:
    for err in result:
      messages.error(req, err)
    return redirect('users:new')

  req.session['user_id'] = result
  return redirect('users:index')

def login(req):
  if req.method != "POST":
    return redirect('users:new')

  valid, result = User.objects.login_user(req.POST)
  print "*"*30
  print result
  if not valid:
    for err in result:
      messages.error(req, err)
    return redirect('users:new')

  req.session['user_id'] = result
  return redirect('users:index')

def logout(req):
  req.session.clear()
  return redirect('users:index')