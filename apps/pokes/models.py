# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse

from django.db import models
from datetime import datetime

import bcrypt
import re
# from ..users.models import User

class PokeManager(models.Manager):
    def add_poke(self, receiver_id):
        try:
            receiver = User.objects.get(id=receiver_id)
            receiver.poked_number += 1
            receiver.save()
            return True
        except:
            return False
    
    def create_poke(self, receiver_id, giver_id):
        giver = User.objects.get(id=giver_id)
        
        try:
            poke = self.create(
                giver=giver.name,
                receiver=User.objects.get(id=receiver_id)
            )

            return True
        except:
            return HttpResponse('poke was not created')
            
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_and_create_user(self, form_data):
        errors = []

        if len(form_data['name']) < 3:
            errors.append(['funny name, ', form_data['name'], '!'])
        if len(form_data['alias']) < 3:
            errors.append([form_data['alias'], " ,that's what you call yourself!?"])
        if not EMAIL_REGEX.match(form_data['email']):
            errors.append('Must use a valid email address')
        if len(form_data['password']) < 3:
            errors.append("that ain't a password!")
        if not form_data['dob']:
            errors.append('you are not one of us, get out!') 
        if form_data['password'] != form_data['confirm']:
            errors.append("Only one password per person, that's the rule")
        if errors:
            return (False, errors)

        try:
            existing_user = self.get(email=form_data['email'])
            errors.append('User already exists.')
            return (False, errors)
        except:
            pw_hash = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt())
            dob = datetime.strptime(form_data['dob'],  '%Y-%m-%d').date()
            user = self.create(
                name=form_data['name'], 
                alias=form_data['alias'],
                email=form_data['email'],
                dob=dob,
                pw_hash=pw_hash
            )
            return (True, user.id)
        
    def login_user(self, form_data):
        errors = []
        try:
            user = self.get(email=form_data['email'])
            if not bcrypt.checkpw(form_data['password'].encode(), user.pw_hash.encode()):
                errors.append('password is invalid')
                return (False, errors)
            return (True, user.id)
        except:
            errors.append('email  is invalid')
            return (False, errors)

class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    dob = models.DateField()
    poked_number = models.IntegerField(default=0)
    pw_hash = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    last_mod = models.DateTimeField(auto_now=True)
    objects = UserManager()

# one to many: each poke is created by one person, one person can create many pokes
# giver is name of person who created poke
# receiver is foreign key, person who was poked
 
class Poke(models.Model):
    giver = models.CharField(max_length=100)
    receiver = models.ForeignKey(User, related_name='users')
    objects = PokeManager()

def __str__(self):
    return self.id


