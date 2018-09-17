from django.shortcuts import render
from Api.models import *
from Api.serializers import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from Api.helper import *
from django.contrib.auth.hashers import check_password

import json

# Create your views here.
@csrf_exempt
def clear_database(request):
    User.objects.all().delete()
    Partner.objects.all().delete()
    Token.objects.all().delete()
    Role.objects.all().delete()
    UserRole.objects.all().delete()
    Airport.objects.all().delete()
    Auto.objects.all().delete()
    AutoType.objects.all().delete()
    CompanyDefault.objects.all().delete()
    Itinerary.objects.all().delete()
    Sublettable.objects.all().delete()
    Park.objects.all().delete()

    return HttpResponse(status = 200)

@csrf_exempt
def specific_park(request, pk):
    authorized = has_authorization(request, 'specific_park')
    user = get_user(request)
    
    try:
        park = Park.objects.get(pk = pk)
    except Park.DoesNotExist:
        error = { 'error': 'Park does not exist.' }
        return JsonResponse(error, status = 404)

    if request.method == 'GET':
        if authorized:
            serializer = ParkSerializer(park, many = False)
            return JsonResponse(serializer.data, safe = False)
        else:
            if user != None:
                if park.itinerary.user.pk == user.pk:
                    serializer = ParkSerializer(park, many = False)
                    return JsonResponse(serializer.data, safe = False)
                else:
                    error = { 'error': 'User does not have required priviledges.' }
                    return JsonResponse(error, status = 403) 
            else:
                error = { 'error': 'User does not have required priviledges.' }
                return JsonResponse(error, status = 403)
    if request.method == 'PATCH':
        if authorized:
            data = JSONParser().parse(request)
        
            serializer = ParkSerializer(park, data = data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status = 200)

            return JsonResponse(serializer.errors, status = 400)
        else:
            if user != None:
                if park.itinerary.user.pk == user.pk:
                    data = JSONParser().parse(request)
        
                    serializer = ParkSerializer(park, data = data, partial = True)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse(serializer.data, status = 200)

                    return JsonResponse(serializer.errors, status = 400)
                else:
                    error = { 'error': 'User does not have required priviledges.' }
                    return JsonResponse(error, status = 403) 
            else:
                error = { 'error': 'User does not have required priviledges.' }
                return JsonResponse(error, status = 403)

    if request.method == 'DELETE':
        if authorized:
            park.delete()
            return HttpResponse(status = 204)   
        else:
            if user != None:
                if park.itinerary.user.pk == user.pk:
                    park.delete()
                    return HttpResponse(status = 204)
                else:
                    error = { 'error': 'User does not have required priviledges.' }
                    return JsonResponse(error, status = 403) 
            else:
                error = { 'error': 'User does not have required priviledges.' }
                return JsonResponse(error, status = 403) 
                
    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def parks(request):
    authorized = has_authorization(request, 'parks')
    user = get_user(request)

    if request.method == 'GET' and authorized:
        parks = Park.objects.all()

        if 'itinerary' in request.GET:
            parks = parks.filter(itinerary = request.GET['itinerary'])

        if 'record_creator' in request.GET:
            parks = parks.filter(record_creator = request.GET['record_creator'])

        serializer = ParkSerializer(parks, many = True)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        data['record_creator'] = user.pk

        if authorized:
            serializer = ParkSerializer(data = data)

            if serializer.is_valid():
                sublet = Sublettable(auto = data['auto'], start = data['start'], end = data['end'], record_creator = data['record_creator'])
                serializer.save()
                sublet.save()
                return JsonResponse(serializer.data, status = 201)

            return JsonResponse(serializer.errors, status = 400)
        else:
            if user != None:
                if 'itinerary' in data:
                    i = Itinerary.objects.filter(pk = data['itinerary'])
                    if len(i) == 1:
                        if i[0].user.pk == user.pk:
                            serializer = ParkSerializer(data = data)

                            if serializer.is_valid():
                                sublet = Sublettable(auto = data['auto'], start = data['start'], end = data['end'], record_creator = data['record_creator'])
                                serializer.save()
                                sublet.save()
                                return JsonResponse(serializer.data, status = 201)

                            return JsonResponse(serializer.errors, status = 400)
                        else:
                            error = { 'error': 'User does not have required priviledges.' }
                            return JsonResponse(error, status = 403)
                    else:
                        error = { 'error': 'Itinerary not found.' }
                        return JsonResponse(error, status = 404)

                serializer = ParkSerializer(data = data)
                return JsonResponse(serializer.errors, status = 400)
            else:
                error = { 'error': 'User does not have required priviledges.' }
                return JsonResponse(error, status = 403)
                
    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

# sublettables should be created automatically and patched by valet
@csrf_exempt
def specific_sublettable(request, pk):
    authorized = has_authorization(request, 'specific_sublettable')

    try:
        sublettable = Sublettable.objects.get(pk = pk)
    except Sublettable.DoesNotExist:
        error = { 'error': 'Sublettable does not exist.' }
        return JsonResponse(error, status = 404)

    if request.method == 'GET' and authorized:
        serializer = SublettableSerializer(sublettable, many = False)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'PATCH' and authorized:
        data = JSONParser().parse(request)
        
        serializer = SublettableSerializer(sublettable, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)

        return JsonResponse(serializer.errors, status = 400)

    if request.method == 'DELETE' and authorized:
        sublettable.delete()
        return HttpResponse(status = 204)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def sublettables(request):
    authorized = has_authorization(request, 'sublettables')

    if request.method == 'GET' and authorized:
        sublettables = Sublettable.objects.all()

        if 'auto' in request.GET:
            sublettables = sublettables.filter(auto = request.GET['auto'])
        
        if 'most_recent' in request.GET:
            if(len(sublettables) != 0):
                s = sublettables[0]
                for sublettable in sublettables:
                    if s < sublettable:
                        s = sublettable

                sublettables = sublettables.filter(pk = s.pk)

        if 'record_creator' in request.GET:
            sublettables = sublettables.filter(record_creator = request.GET['record_creator'])

        serializer = SublettableSerializer(sublettables, many = True)
        return JsonResponse(serializer.data, safe = False)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def specific_itinerary(request, pk):
    authorized = has_authorization(request, 'specific_itinerary')
    user = get_user(request)

    if user == None:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)
    
    try:
        itinerary = Itinerary.objects.get(pk = pk)
    except Itinerary.DoesNotExist:
        error = { 'error': 'Itinerary does not exist.' }
        return JsonResponse(error, status = 404)

    if request.method == 'GET':
        if authorized:
            serializer = ItinerarySerializer(itinerary, many = False)
            return JsonResponse(serializer.data, safe = False)
        else:
            if user.pk == itinerary.user.pk:
                serializer = ItinerarySerializer(itinerary, many = False)
                return JsonResponse(serializer.data, safe = False)

            error = { 'error': 'User does not have required priviledges.' }
            return JsonResponse(error, status = 403)

    if request.method == 'PATCH':
        data = JSONParser().parse(request)
        if 'record_creator' in data:
            del data['record_creator']

        if authorized:
            serializer = ItinerarySerializer(itinerary, data = data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status = 200)

            return JsonResponse(serializer.errors, status = 400)
        else:
            if user.pk == itinerary.user.pk:
                serializer = ItinerarySerializer(itinerary, data = data, partial = True)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status = 200)

                return JsonResponse(serializer.errors, status = 400)

            error = { 'error': 'User does not have required priviledges.' }
            return JsonResponse(error, status = 403)

    if request.method == 'DELETE':
        if authorized:
            itinerary.delete()
            return HttpResponse(status = 204)
        else:
            if user.pk == itinerary.user.pk:
                itinerary.delete()

            error = { 'error': 'User does not have required priviledges.' }
            return JsonResponse(error, status = 403)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)
            
@csrf_exempt
def itineraries(request):
    authorized = has_authorization(request, 'itineraries')
    user = get_user(request)

    if request.method == 'GET' and authorized:
        itineraries = Itinerary.objects.all()

        if 'user' in request.GET:
            itineraries = itineraries.filter(user = request.GET['user'])

        if 'record_creator' in request.GET:
            itineraries = itineraries.filter(record_creator = request.GET['record_creator'])

        serializer = ItinerarySerializer(itineraries, many = True)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        data['record_creator'] = user.pk

        if authorized:
            if not 'user' in data:
                data['user'] = user.pk

            serializer = ItinerarySerializer(data = data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status = 201)

            return JsonResponse(serializer.errors, status = 400)
        else:
            if user != None:
                data['user'] = user.pk

                serializer = ItinerarySerializer(data = data)

                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status = 201)

                return JsonResponse(serializer.errors, status = 400)
            else:
                error = { 'error': 'User does not have required priviledges.' }
                return JsonResponse(error, status = 403)
                
    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def company_defaults(request):
    authorized = has_authorization(request, 'company_defaults')
    
    company_defaults = CompanyDefault.objects.all()
    if len(company_defaults) == 0:
        company_defaults = CompanyDefault()
        company_defaults.save()
    else:
        company_defaults = company_defaults[0]

    if request.method == 'GET' and authorized:
        serializer = CompanyDefaultSerializer(company_defaults, many = False)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'PATCH' and authorized:
        data = JSONParser().parse(request)
        
        serializer = CompanyDefaultSerializer(company_defaults, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)

        return JsonResponse(serializer.errors, status = 400)
    
    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def specific_user_autos(request, pk):
    # only an administrator or a specific user will be able to alter data
    authorized = has_authorization(request, 'specific_user_autos')
    user = get_user(request)

    if user != None and user.pk == pk:
        authorized = True

    if request.method == 'GET' and authorized:
        autos = Auto.objects.filter(user = User.objects.get(pk = pk))
        serializer = GET_AutoSerializer(autos, many = True)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'POST' and authorized:
        data = JSONParser().parse(request)

        if not has_authorization(request, 'specific_user_autos'):
            if authorized:
                data['user'] = pk
            else:
                error = { 'error': 'User not logged in.' }
                return JsonResponse(error, status = 403)
        else:
            data['user'] = pk

        serializer = POST_AutoSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)

        return JsonResponse(serializer.errors, status = 400)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def specific_auto(request, pk):
    authorized = has_authorization(request, 'specific_auto')
    user = get_user(request)

    try:
        auto = Auto.objects.get(pk = pk)
    except Auto.DoesNotExist:
        error = { 'error': 'Auto does not exist.' }
        return JsonResponse(error, status = 404)

    if user != None and auto.user == user:
        authorized = True

    if request.method == 'GET' and authorized:
        serializer = GET_AutoSerializer(auto, many = False)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'PATCH' and authorized:
        data = JSONParser().parse(request)

        if not authorized:
            if user != None:
                data['user'] = user.pk
            else:
                error = { 'error': 'User not logged in.' }
                return JsonResponse(error, status = 403)
        else:
            if not 'user' in data:
                data['user'] = user.pk

        serializer = POST_AutoSerializer(auto, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)

        return JsonResponse(serializer.errors, status = 400)

    if request.method == 'DELETE' and authorized:
        auto.delete()
        return HttpResponse(status = 204)
    
    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def autos(request):
    authorized = has_authorization(request, 'autos')

    if request.method == 'GET' and authorized:
        autos = Auto.objects.all()

        if 'user' in request.GET:
            autos = autos.filter(user = request.GET['user'])

        serializer = GET_AutoSerializer(autos, many = True)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'POST':
        data = JSONParser().parse(request)

        user = get_user(request)
        if not authorized:
            if user != None:
                data['user'] = user.pk
            else:
                error = { 'error': 'User not logged in.' }
                return JsonResponse(error, status = 403)
        else:
            if not 'user' in data:
                data['user'] = user.pk

        serializer = POST_AutoSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)

        return JsonResponse(serializer.errors, status = 400)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)   

@csrf_exempt
def specific_autotype(request, pk):
    authorized = has_authorization(request, 'specific_autotype')

    try:
        autotype = AutoType.objects.get(pk = pk)
    except AutoType.DoesNotExist:
        error = { 'error': 'Auto Type does not exist.' }
        return JsonResponse(error, status = 404)

    if request.method == 'GET' and authorized:
        serializer = AutoTypeSerializer(autotype, many = False)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'PATCH' and authorized:
        data = JSONParser().parse(request)

        serializer = AutoTypeSerializer(autotype, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)

        return JsonResponse(serializer.errors, status = 400)

    if request.method == 'DELETE' and authorized:
        autotype.delete()
        return HttpResponse(status = 204)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def autotypes(request):
    authorized = has_authorization(request, 'autotypes')

    if request.method == 'GET' and authorized:
        autotypes = AutoType.objects.all()

        if 'make' in request.GET:
            autotypes = autotypes.filter(make = request.GET['make'])

        if 'model' in request.GET:
            autotypes = autotypes.filter(model = request.GET['model'])
        
        if 'year' in request.GET:
            autotypes = autotypes.filter(year = request.GET['year'])

        serializer = AutoTypeSerializer(autotypes, many = True)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'POST' and authorized:
        data = JSONParser().parse(request)
        serializer = AutoTypeSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)

        return JsonResponse(serializer.errors, status = 400)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)


@csrf_exempt
def specific_airport(request, pk):
    authorized = has_authorization(request, 'specific_airport')

    try:
        airport = Airport.objects.get(airport_code = pk)
    except Airport.DoesNotExist:
        error = { 'error': 'Airport does not exist.' }
        return JsonResponse(error, status = 404)

    if request.method == 'GET' and authorized:
        serializer = AirportSerializer(airport, many = False)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'PATCH' and authorized:
        data = JSONParser().parse(request)

        serializer = AirportSerializer(airport, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)

        return JsonResponse(serializer.errors, status = 400)

    if request.method == 'DELETE' and authorized:
        airport.delete()
        return HttpResponse(status = 204)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def airports(request):
    authorized = has_authorization(request, 'airports')

    if request.method == 'GET' and authorized:
        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many = True)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'POST' and authorized:
        data = JSONParser().parse(request)
        serializer = AirportSerializer(data = data)

        if len(CompanyDefault.objects.all()) == 0:
            CompanyDefault().save()

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)

        return JsonResponse(serializer.errors, status = 400)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def specific_partner_users(request, pk):
    authorized = has_authorization(request, 'specific_partner_users')
    
    try:
        partner = Partner.objects.get(pk = pk)
    except Partner.DoesNotExist:
        error = { 'error': 'Partner does not exist.' }
        return JsonResponse(error, status = 404)

    if request.method == 'GET' and authorized:
        users = User.objects.filter(partner = partner)
        serializer = UserSerializer(users, many = True)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'POST' and authorized:
        data = JSONParser().parse(request)
        data['partner'] = pk

        serializer = UserSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)

        return JsonResponse(serializer.errors, status = 400)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def specific_partner(request, pk):
    authorized = has_authorization(request, 'specific_partner')

    try:
        partner = Partner.objects.get(pk = pk)
    except Partner.DoesNotExist:
        error = { 'error': 'Partner does not exist.' }
        return JsonResponse(error, status = 404)

    if request.method == 'GET' and authorized:
        serializer = PartnerSerializer(partner, many = False)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'PATCH' and authorized:
        data = JSONParser().parse(request)

        serializer = PartnerSerializer(partner, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)

        return JsonResponse(serializer.errors, status = 400)

    if request.method == 'DELETE' and authorized:
        partner.delete()
        return HttpResponse(status = 204)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def partners(request):
    authorized = has_authorization(request, 'partners')

    if request.method == 'GET' and authorized:
        partners = Partner.objects.all()

        if 'airport' in request.GET:
            partners = partners.filter(airport = request.GET['airport'])

        serializer = PartnerSerializer(partners, many = True)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'POST' and authorized:
        data = JSONParser().parse(request)
        serializer = PartnerSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)

        return JsonResponse(serializer.errors, status = 400)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def specific_role(request, pk):
    authorized = has_authorization(request, 'specific_role')

    try:
        role = Role.objects.get(name = pk)
    except Role.DoesNotExist:
        error = { 'error': 'Role does not exist.' }
        return JsonResponse(error, status = 404)

    if request.method == 'GET' and authorized:
        serializer = RoleSerializer(role, many = False)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'DELETE' and authorized:
        role.delete()
        return HttpResponse(status = 204)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def specific_user_role(request, pk):
    # only an administrator or a specific user will be able to alter data
    authorized = has_authorization(request, 'specific_user_role')
    user = get_user(request)

    try:
        role = UserRole.objects.get(pk = pk)
    except UserRole.DoesNotExist:
        error = { 'error': 'Role does not exist.' }
        return JsonResponse(error, status = 404)

    if user != None and role.user == user:
        authorized = True

    if request.method == 'GET' and authorized:
        serializer = UserRoleSerializer(role, many = True)
        return JsonResponse(serializer.data, safe = False)\

    if request.method == 'DELETE' and has_authorization(request, 'specific_user_role'):
        role.delete()
        return HttpResponse(status = 204)
    
    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def specific_user_user_roles(request, pk):
    # only an administrator or a specific user will be able to alter data
    authorized = has_authorization(request, 'specific_user_user_roles')
    user = get_user(request)
    if user != None and user.pk == pk:
        authorized = True

    if request.method == 'GET' and authorized:
        roles = UserRole.objects.filter(user = User.objects.get(pk = pk))
        serializer = UserRoleSerializer(roles, many = True)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'POST' and has_authorization(request, 'specific_user_user_roles'):
        data = JSONParser().parse(request)
        data['user'] = pk

        serializer = UserRoleSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)

        return JsonResponse(serializer.errors, status = 400)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def specific_user(request, pk):
    # only an administrator or a specific user will be able to alter data
    authorized = has_authorization(request, 'specific_user')
    user = get_user(request)
    if user != None and user.pk == pk:
        authorized = True

    try:
        user = User.objects.get(pk = pk)
    except User.DoesNotExist:
        error = { 'error': 'User does not exist.' }
        return JsonResponse(error, status = 404)

    if request.method == 'GET' and authorized:
        serializer = UserSerializer(user, many = False)
        return JsonResponse(serializer.data, safe = False)

    if request.method == 'PATCH' and authorized:
        data = JSONParser().parse(request)
        
        # here we need to do special overwrites if the user is not an administrator
        if not has_authorization(request, 'specific_user') and 'partner' in data:
            data['partner'] = user.partner.pk

        serializer = UserSerializer(user, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)

        return JsonResponse(serializer.errors, status = 400)

    if request.method == 'DELETE' and authorized:
        user.delete()
        return HttpResponse(status = 204)
    
    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def user_roles(request):
    # only an administrator will be able to create user roles
    authorized = has_authorization(request, 'user_roles')
    if request.method == 'POST' and authorized:
        data = JSONParser().parse(request)
        serializer = UserRoleSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)

        return JsonResponse(serializer.errors, status = 400)

    if request.method == 'GET' and authorized:
        roles = UserRole.objects.all()

        if 'user' in request.GET:
            roles = roles.filter(user = request.GET['user'])

        serializer = UserRoleSerializer(roles, many = True)

        return JsonResponse(serializer.data, safe = False)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def roles(request):
    # only an administrator will be allowed to view all the possible roles
    authorized = has_authorization(request, 'user_roles')
    if request.method == 'POST' and authorized:
        data = JSONParser().parse(request)
        serializer = RoleSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)

        return JsonResponse(serializer.errors, status = 400)

    if request.method == 'GET' and authorized:
        roles = Role.objects.all()

        if 'name' in request.GET:
            roles = roles.filter(name = request.GET['name'])

        serializer = RoleSerializer(roles, many = True)

        return JsonResponse(serializer.data, safe = False)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def logout(request):
    try:
        token = request.META['HTTP_AUTHENTICATION']
    except KeyError:
        error = { 'error': 'You did not provide a valid token.' }
        return JsonResponse(error, status = 400)

    tokens = Token.objects.filter(token = token)
    if len(tokens) == 0:
        error = { 'error': 'You are already logged out.' }
        return JsonResponse(error, status = 400)

    tokens[0].delete()
    return HttpResponse(status = 204)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        if not 'email' in data or data['email'] == '':
            error = { 'email': 'Must provide email.' }
            return JsonResponse(error, status = 400)

        if not 'password' in data or data['password'] == '':
            error = { 'password': 'Must provide password.' }
            return JsonResponse(error, status = 400)

        try:
            user = User.objects.get(email = data['email'])
        except User.DoesNotExist:
            error = { 'email': 'Does not exist.' }
            return JsonResponse(error, status = 404)
        
        if check_password(data['password'] + user.salt, user.password):
            token = generate_token(20, user)
            serializer = TokenSerializer(token, many = False)
            return JsonResponse(serializer.data, safe = False)

        error = { 'password': 'Incorrect password.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)

@csrf_exempt
def users(request):
    # anyone can make a user, but only an administrator can get users
    authorized = has_authorization(request, 'users')
    if request.method == 'POST':
        data = JSONParser().parse(request)

        if 'partner' in data:
            data['partner'] = None

        serializer = UserSerializer(data = data)

        if serializer.is_valid():
            serializer.save()

            # we need to assign initial roles
            consumer = Role.objects.filter(name = 'CONSUMER')
            if len(consumer) == 0:
                Role(name = 'CONSUMER', description = 'Application user.').save()
                consumer = Role.objects.filter(name = 'CONSUMER')
                
                Role(name = 'ADMINISTRATOR', description = 'Application owner.').save()
                administrator = Role.objects.filter(name = 'ADMINISTRATOR')

                administrator = administrator[0]
                UserRole(role = administrator, user = User.objects.get(pk = serializer.data['pk'])).save()

            consumer = consumer[0]
            UserRole(role = consumer, user = User.objects.get(pk = serializer.data['pk'])).save()

            sendEmail(serializer.data['email'], 'validate')
            return JsonResponse(serializer.data, status = 201)

        return JsonResponse(serializer.errors, status = 400)

    if request.method == 'GET' and authorized:
        users = User.objects.all()

        if 'partner' in request.GET:
            users = users.filter(partner = request.GET['partner'])

        serializer = UserSerializer(users, many = True)

        return JsonResponse(serializer.data, safe = False)

    if authorized == False:
        error = { 'error': 'User does not have required priviledges.' }
        return JsonResponse(error, status = 403)

    error = { 'error': 'Request method is unsupported.' }
    return JsonResponse(error, status = 400)