from rest_framework import serializers

from .models import Client, Company


class ContactSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    company = serializers.JSONField()



#client model serializer 
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        #set of the model class
        model = Client
        #set of the usable fields
        fields = (
            'id',
            'company',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            
        )


#company model serializer
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        #set of the model class
        model = Company
        #set of the usable fields
        fields = (
            'id',
            'name',
        )