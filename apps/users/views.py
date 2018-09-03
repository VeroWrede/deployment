# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..pokes.models import User, Poke
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages


def index(req):
  if 'user_id' not in req.session:
    return redirect('users:new')

  user_id = req.session['user_id']
  pokers = Poke.objects.filter(receiver__in=User.objects.filter(id=user_id).order_by('poked_number'))
  # grouped_pokers =Poke.objects.raw(
  #                                 SELECT COUNT(
  #                                         SELECT * from Poke
  #                                         WHERE receiver = logged_in_user)
  #                                 GROUP BY poker)
  context = {
    'user': User.objects.get(id=user_id),
    'count': pokers.count(),
    'all': User.objects.exclude(id=user_id),
    'pokes': User.objects.filter(id=user_id).filter(users__in=Poke.objects.all()),
    'pokers': pokers
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