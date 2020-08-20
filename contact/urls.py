from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
#views
from . import views

#application namespace
app_name = 'contact'

#urls root
urlpatterns = [
    path('', views.ContactsListView.as_view(), name='contacts_list'),#contact listing view
    path('contact/<int:client_id>/', views.ContactDetailView.as_view(), name='detail'),#contact detail view
    path('contact', views.ClientSearchView.as_view(), name='search_contact'),#client searching view
    path('login/', obtain_auth_token, name='obtain-token'),
]