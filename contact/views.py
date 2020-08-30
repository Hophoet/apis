from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
#
#from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, 
HTTP_201_CREATED)
#
from .serializers import (ClientSerializer, CompanySerializer,
 ContactSerializer)
from .models import Client, Company
from .forms import AddContactForm, AddContactError



#call contact json list builder
def contactsJsonBuilder(clients):
    contacts = [ ]
    for client in clients:
        contactJson = {
            'first_name':client.first_name,
            'last_name':client.last_name,
            'phone_number':client.phone_number,
            'email':client.email,
            'company':{
                'name':client.company.name
            }
        }
        contacts.append(contactJson)
    return contacts
    
#single contact json builder
def contactJsonBuilder(client):
    contactJson = {
            'first_name':client.first_name,
            'last_name':client.last_name,
            'phone_number':client.phone_number,
            'email':client.email,
            'company':{
                'name':client.company.name
            }
        }

    return contactJson


#Contact list view
class ContactsListView(APIView):
    #set of the permission classes
    permission_classes = (IsAuthenticated,)
    #get request method
    def get(self, request, *args, **kwargs):
        #get of all the available clients
        clients = Client.objects.all() 
        contacts = contactsJsonBuilder(clients)
        #building the serializer with the get clients
        #return the response
        return Response(contacts)



#contact detail view
class ContactDetailView(APIView):
    #set of the permission
    permission_classes = (IsAuthenticated,)
    #get request method
    def get(self, request, *args, **kwargs):
        #build client and company object with client id
        client_id = kwargs.get('client_id')
        try:
            client = Client.objects.get(id=client_id)
        except ObjectDoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND, data={'error':'contact not found'})

        contact = contactJsonBuilder(client)
    
        #build serializers by the get objects
        contact_serializer = ContactSerializer(contact)
        #return the response
        return Response(contact_serializer.data)

#client seart view
class ClientSearchView(APIView):
    #set of the permission classes
    #permission_classes = (IsAuthenticated,)
    #get request method
    def get(self, request, *args, **kwargs):
        #get of the url query parameter
        query = request.GET.get('query')
        #check the existence of the query
        if not query:
            #return 4040 status error 
            return Response(status=404)

        else:
            #search the clients by there first_name
            clients = Client.objects.filter(first_name__icontains=query)
        if not clients.exists():
            #search the clients, there last_name
            clients = Client.objects.filter(last_name__icontains=query)
        if not clients.exists():
            #return 4040 status error 
            return Response(status=404)
        #build serializer with the get clients
        clients = ClientSerializer(clients, many=True)
        #return the response
        return Response(clients.data)

#add contact request errors builder
def add_contact_request_errors_json_builder(errors_dict):
    errors_json = {}
    for key, value in errors_dict:
        errors_json[key] = {error for error in value}
    return errors_json

#save contact view
class AddContactView(APIView):
    permission_classes = (IsAuthenticated,)
    

    #post
    def post(self, request, *args, **kwargs):
        #create contact from with POST request data
        add_contact_form = AddContactForm(request.POST, error_class=AddContactError)
        #contact form not valid case
        if not add_contact_form.is_valid():
            #build and return of the error
            errors_json = add_contact_request_errors_json_builder(add_contact_form.errors.items())
            return Response(errors_json, status=HTTP_400_BAD_REQUEST)
        #valid case
        valid_data = add_contact_form.cleaned_data
        company_name = valid_data['company']['name']
        first_name = valid_data['first_name']
        last_name = valid_data['last_name']
        email = valid_data['email']
        phone_number = valid_data['phone_number']
        #try to get the company (exists case)
        try:
            company = Company.objects.get(name=company_name)
            Client.objects.create(
                first_name=first_name, last_name=last_name, 
                email=email, phone_number=phone_number, company=company
            )
        #company not exists yet case
        except ObjectDoesNotExist:
            company = Company.objects.create(name=company_name)
            Client.objects.create(
                first_name=first_name, last_name=last_name, 
                email=email, phone_number=phone_number, company=company
            )

        return Response({'detail':'contact added successfully'}, status=HTTP_201_CREATED)