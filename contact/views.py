from django.shortcuts import render
from django.http import JsonResponse

#
#from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
#
from .serializers import ClientSerializer, CompanySerializer
from .models import Client

class AllContactView(APIView):
    
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        qs = Client.objects.all()
       
        serializer = ClientSerializer(qs, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


#Contact list view
class ContactsListView(APIView):
    #set of the permission classes
    permission_classes = (IsAuthenticated,)
    #get request method
    def get(self, request, *args, **kwargs):
        #get of all the available clients
        clients = Client.objects.all() 
        #building the serializer with the get clients
        serializer = ClientSerializer(clients, many=True)
        #return the response
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        pass
        # serializer = PostSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)

#contact detail view
class ContactDetailView(APIView):
    #set of the permission
    #permission_classes = (IsAuthenticated,)
    #get request method
    def get(self, request, *args, **kwargs):
        #build client and company object with client id
        client_id = kwargs.get('client_id')
        client = Client.objects.get(id=client_id)
        company = client.company
        #build serializers by the get objects
        client_serializer = ClientSerializer(client)
        company_serializer = CompanySerializer(company)
        #return the response
        return Response(data=(client_serializer.data, company_serializer.data))

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
