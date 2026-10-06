import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import CarMake, CarModel
from . import services

# List of all US States for the filter dropdown
ALL_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina",
    "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
    "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
    "Wisconsin", "Wyoming"
]

def index(request):
    """
    Main home view: displays all dealerships or filtered by query parameter `state`.
    """
    selected_state = request.GET.get('state', '').strip()
    if selected_state and selected_state.lower() != 'all':
        dealers = services.get_dealers(state=selected_state)
    else:
        dealers = services.get_dealers()
        selected_state = ''

    # Get distinct states available from dealers list or standard list
    states = sorted(list(set([d.get('state') for d in services.get_dealers() if d.get('state')])))
    if not states:
        states = ALL_STATES

    context = {
        'dealers': dealers,
        'dealers_json': json.dumps(dealers),
        'states': states,
        'selected_state': selected_state,
        'total_dealers': len(dealers),
    }
    return render(request, 'dealerships/index.html', context)


def dealers_by_state(request, state):
    """
    View to display dealerships filtered by state with URL path visible: e.g. /dealers/Kansas
    """
    dealers = services.get_dealers(state=state)
    states = sorted(list(set([d.get('state') for d in services.get_dealers() if d.get('state')])))
    if not states:
        states = ALL_STATES

    context = {
        'dealers': dealers,
        'dealers_json': json.dumps(dealers),
        'states': states,
        'selected_state': state,
        'total_dealers': len(dealers),
    }
    return render(request, 'dealerships/index.html', context)


def about(request):
    """
    Static page: About Us
    """
    return render(request, 'dealerships/about.html')


def contact(request):
    """
    Static page: Contact Us
    """
    if request.method == 'POST':
        messages.success(request, "¡Gracias por contactarnos! Tu mensaje ha sido enviado correctamente.")
        return redirect('dealerships:contact')
    return render(request, 'dealerships/contact.html')


def login_request(request):
    """
    User authentication Login view
    """
    if request.user.is_authenticated:
        return redirect('dealerships:index')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"¡Bienvenido de nuevo, {user.username}! Has iniciado sesión con éxito.")
            next_url = request.GET.get('next', 'dealerships:index')
            return redirect(next_url)
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")

    return render(request, 'dealerships/login.html')


def logout_request(request):
    """
    User logout view: Logs out user and triggers an explicit logout alert message
    """
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente. ¡Te esperamos pronto!")
    return redirect('dealerships:index')


def signup_request(request):
    """
    User registration Sign-Up view
    """
    if request.user.is_authenticated:
        return redirect('dealerships:index')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()

        if password != password_confirm:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'dealerships/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, f"El nombre de usuario '{username}' ya está en uso.")
            return render(request, 'dealerships/register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)
        messages.success(request, f"¡Cuenta creada con éxito! Bienvenido a la plataforma, {username}.")
        return redirect('dealerships:index')

    return render(request, 'dealerships/register.html')


def dealer_details(request, dealer_id):
    """
    Displays full details for a dealership along with customer reviews and sentiment analysis
    """
    dealer = services.get_dealer_by_id(dealer_id)
    if not dealer:
        messages.error(request, f"No se encontró el concesionario con ID {dealer_id}.")
        return redirect('dealerships:index')

    reviews = services.get_reviews_by_dealer_id(dealer_id)

    # Sentiment statistics
    sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
    for r in reviews:
        sent = r.get('sentiment', 'neutral').lower()
        if sent in sentiment_counts:
            sentiment_counts[sent] += 1

    context = {
        'dealer': dealer,
        'reviews': reviews,
        'total_reviews': len(reviews),
        'sentiments': sentiment_counts,
    }
    return render(request, 'dealerships/dealer_detail.html', context)


@login_required(login_url='dealerships:login')
def add_review(request, dealer_id):
    """
    View to submit a new review for a dealership. Requires authenticated user.
    """
    dealer = services.get_dealer_by_id(dealer_id)
    if not dealer:
        messages.error(request, f"No se encontró el concesionario con ID {dealer_id}.")
        return redirect('dealerships:index')

    car_makes = CarMake.objects.prefetch_related('models').all()

    if request.method == 'POST':
        review_content = request.POST.get('review', '').strip()
        purchase = request.POST.get('purchase') == 'on'
        purchase_date = request.POST.get('purchase_date', '')
        car_make_name = request.POST.get('car_make', '')
        car_model_name = request.POST.get('car_model', '')
        car_year_str = request.POST.get('car_year', '2024')

        try:
            car_year = int(car_year_str)
        except ValueError:
            car_year = 2024

        reviewer_name = request.user.get_full_name() or request.user.username

        payload = {
            'name': reviewer_name,
            'dealership': int(dealer_id),
            'review': review_content,
            'purchase': purchase,
            'purchase_date': purchase_date,
            'car_make': car_make_name,
            'car_model': car_model_name,
            'car_year': car_year
        }

        result = services.post_review(payload)
        if result:
            messages.success(request, "¡Tu reseña ha sido publicada y analizada con éxito!")
            return redirect('dealerships:dealer_details', dealer_id=dealer_id)
        else:
            messages.error(request, "Hubo un error al enviar tu reseña al microservicio. Intenta de nuevo.")

    context = {
        'dealer': dealer,
        'car_makes': car_makes,
    }
    return render(request, 'dealerships/add_review.html', context)


def get_cars_api(request):
    """
    API endpoint returning car makes and models JSON
    """
    makes = CarMake.objects.all()
    data = []
    for make in makes:
        data.append({
            'make_id': make.id,
            'make_name': make.name,
            'models': [{'id': m.id, 'name': m.name, 'type': m.type, 'year': m.year} for m in make.models.all()]
        })
    return JsonResponse({'cars': data})
