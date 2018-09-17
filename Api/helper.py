from Api.models import *
from django.contrib.auth.hashers import make_password

import random
import json
import os
import binascii

def sendEmail(email, reason):
    pass

def random_string(length):
    characters = 'abcdefghijklmnopqrstuvwxyz'
    characters += characters.upper()
    characters += '[~`!@#$%^&*()_-+={}|/",.<>?]'

    return ''.join(random.choice(characters) for m in range(length))

def generate_token(length, user):
    value = binascii.hexlify(os.urandom(length)).decode()
    while(len(Token.objects.filter(token = value)) != 0):
        value = binascii.hexlify(os.urandom(length)).decode()

    currentToken = Token.objects.filter(user = user)
    if len(currentToken) != 0:
        currentToken[0].delete()

    t = Token(token = value, user = user)
    t.save()
    return t

def get_user(request):
    try:
        token = request.META['HTTP_AUTHENTICATION']
    except KeyError:
        return None

    tokens = Token.objects.filter(token = token)
    if len(tokens) == 0:
        return None
    
    return tokens[0].user

def get_roles(request):
    user = get_user(request)
    if user == None:
        return []

    roles = UserRole.objects.filter(user = user)

    role_list = []
    for role in roles:
        role_list.append(role.role.name)

    return role_list

def has_authorization(request, view):
    roles = get_roles(request)
    with open('PRIVILEDGES.json') as data_file:    
        data = json.load(data_file)

    if not request.method in data[view]:
        return None

    for role in roles:
        if role in data[view][request.method]:
            return True

    return False

def charge_card(card, amount):
    pass