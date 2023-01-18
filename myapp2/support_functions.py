from myapp2.models import*

def get_currency_list():
    currency_list = list()
    import requests
    from bs4 import BeautifulSoup
    url = "https://thefactfile.org/countries-currencies-symbols/"
    response = requests.get(url)
    if not response.status_code == 200:
        return currency_list
    soup = BeautifulSoup(response.content)
    data_lines = soup.find_all('tr')
    for line in data_lines:
        try:
            detail = line.find_all('td')
            currency = detail[2].get_text().strip()
            iso = detail[3].get_text().strip()
            if (currency,iso) in currency_list:
                continue
                currency_list.append((currency,iso))
        except:
            continue
    return currency_list



def add_currencies(currency_list):
    for currency in currency_list:
        currency_name = currency[0]
        currency_symbol = currency[1]
        try:
            c= Currency.objects.get(iso=currency_symbol)
        except:
            c = Currency(long_name=currency_name, iso=currency_symbol)
            c.save()
        c.name = currency_name
        c.save() #To test out the code, replace this by print(c)

from django.contrib import admin
# Register your models here.
from myapp2.models import Currency, Holding
class HoldingInLine(admin.TabularInline):
    fields = ('iso','value','buy_data')
    model = Holding
    extra = 0
class CurrencyAdmin(admin.ModelAdmin):
    fields = ('long_name','iso')
    inlines = [HoldingInLine]
admin.site.register(Currency,CurrencyAdmin)