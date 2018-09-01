# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse

from django.db import models
# from ..users.models import User

class PokeManager(models.Manager):
    # can't import User into this file so logic will be in views
    def add_poke(self, receiver_id):
        try:
            receiver = User.objects.get(id=receiver_id)
            receiver.poked_number += 1
            receiver.save()
            return True
        except:
            return False
    # get giver
    # get receiver
    # create object

    def create_poke(self, receiver_id, giver_id):
        giver = User.objects.get(id=giver_id)
            
        try:
            poke = self.create(
                giver=giver.name,
                receiver=User.objects.get(id=receiver_id)
            )
            return True
        except:
            return False
            

# one to many: each poke is created by one person, one person can create many pokes
# giver is name of person who created poke
# receiver is foreign key, person who was poked
class Poke(models.Model):
    giver = models.CharField(max_length=100)
    receiver = models.ForeignKey(User, related_name='pokes')
    objects = PokeManager()

def __str__(self):
    return self.id
    
def Temp():
    pass
