import uuid
import random
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from .forms import PlaceForm

DEFAULT_IMAGE = 'places/images/sakura.jpg'


def _get_places_from_session(request):
    return request.session.get('places', [])


def _save_places_to_session(request, places):
    request.session['places'] = places
    request.session.modified = True


def index(request):
    return render(request, 'places/index.html', {})


def places_list(request):
    places = _get_places_from_session(request)
    places_sorted = sorted(places, key=lambda p: p.get('created_at', ''), reverse=True)
    return render(request, 'places/places_list.html', {'places': places_sorted})


def place_detail(request, place_id):
    places = _get_places_from_session(request)
    place = next((p for p in places if p['id'] == place_id), None)
    if place is None:
        return redirect('places:places_list')
    return render(request, 'places/place_detail.html', {'place': place})


@require_http_methods(['GET', 'POST'])
def add_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            places = _get_places_from_session(request)
            rating = int(form.cleaned_data['rating'])
            new_place = {
                'id': str(uuid.uuid4()),
                'name': form.cleaned_data['name'],
                'full_description': form.cleaned_data['full_description'] or '',
                'short_description': (form.cleaned_data['full_description'] or '')[:120],
                'type': form.cleaned_data.get('type') or 'Невідомо',
                'location': form.cleaned_data.get('location') or '',
                'rating': rating,
                'created_at': timezone.now().isoformat(),
                'image': DEFAULT_IMAGE,
            }
            places.append(new_place)
            _save_places_to_session(request, places)
            return redirect('places:places_list')
    else:
        form = PlaceForm()
    return render(request, 'places/add_place.html', {'form': form})


@require_http_methods(['POST'])
def pick_place(request):
    places = _get_places_from_session(request)
    if not places:
        return render(request, 'places/index.html', {'error': 'Список порожній. Додайте місце.'})
    weights = [p.get('rating', 1) for p in places]
    selected = random.choices(places, weights=weights, k=1)[0]
    return render(request, 'places/index.html', {'preview': selected})




