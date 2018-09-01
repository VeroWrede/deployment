# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import Poke, User


# receiver_id refers to the id of a person listed (receiver), not the logged in user
def poke(req, receiver_id):
    valid = Poke.objects.add_poke(receiver_id)
    if not valid:
        return HttpResponse('poke was not added')

    giver_id = req.session['user_id']
    valid = Poke.objects.create_poke(receiver_id, giver_id)
    
    if not valid:
        return HttpResponse('model couldnt find receciver')
    
    return redirect('users:index')