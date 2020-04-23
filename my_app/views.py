import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup

from .models import Search


BASE_CRAIGLIST_URL = 'https://bulgaria.craigslist.org/search/?query={}'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    # Get search and store it
    search = request.POST.get('search')
    Search.objects.create(search=search)

    # Get data from the page as HTML
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text

    # Use BeautifulSoup to filter HTML & generate data for the template
    soup = BeautifulSoup(data, features='html.parser')
    response_data = soup.find_all('li', {'class': 'result-row'})
    results = []
    for item in response_data:
        title = item.find(class_='result-title').text
        url = item.find('a').get('href')
        results.append({'title': title, 'url': url})

    context = {'search': search, 'results': results}
    return render(request, 'my_app/new_search.html', context)
