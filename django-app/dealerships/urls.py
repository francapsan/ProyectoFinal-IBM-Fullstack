from django.urls import path
from . import views

app_name = 'dealerships'

urlpatterns = [
    # Main dealership views (with state filtering)
    path('', views.index, name='index'),
    path('dealers/', views.index, name='dealers'),
    path('dealers/<str:state>/', views.dealers_by_state, name='dealers_by_state'),
    path('dealers/state/<str:state>/', views.dealers_by_state, name='dealers_by_state_alt'),
    
    # Dealer details & reviews
    path('dealer/<int:dealer_id>/', views.dealer_details, name='dealer_details'),
    path('dealer/<int:dealer_id>/add-review/', views.add_review, name='add_review'),
    
    # Static content
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # User Authentication
    path('login/', views.login_request, name='login'),
    path('login', views.login_request, name='login_no_slash'),
    path('logout/', views.logout_request, name='logout'),
    path('logout', views.logout_request, name='logout_no_slash'),
    path('signup/', views.signup_request, name='signup'),
    path('register/', views.signup_request, name='register'),
    path('register', views.signup_request, name='register_no_slash'),
    
    # API endpoints for Capstone tasks & React
    path('api/cars/', views.get_cars_api, name='get_cars_api'),
    path('get_cars/', views.get_cars_api, name='get_cars'),
    path('get_cars', views.get_cars_api, name='get_cars_no_slash'),
    path('getcars', views.get_cars_api, name='getcars'),
    path('get_dealers/', views.get_dealers_api, name='get_dealers_api'),
    path('get_dealers', views.get_dealers_api, name='get_dealers_api_no_slash'),
    path('get_dealers/<str:state>/', views.get_dealers_by_state_api, name='get_dealers_by_state_api'),
    path('get_dealers/<str:state>', views.get_dealers_by_state_api, name='get_dealers_by_state_api_no_slash'),
    path('get_reviews/<int:dealer_id>/', views.get_dealer_reviews_api, name='get_dealer_reviews_api'),
    path('get_reviews/<int:dealer_id>', views.get_dealer_reviews_api, name='get_dealer_reviews_api_no_slash'),
]
