from django.contrib.auth import get_user_model
from django.db import models

#User model 
User = get_user_model()



#Company(entreprise) model
class Company(models.Model):
    name = models.CharField(max_length=100)


    #model printing string
    def __str__(self):
        return self.name

#Client representation model
class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField() 
    phone_number = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    #model printting string
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

