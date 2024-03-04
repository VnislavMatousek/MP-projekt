import math

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import TaxForm, TaxFormRok,HistoryFilterForm

from .models import CalculationResult, CalculationResultYear


def index(request):
    return render(request, "index.html")

def calculate_tax(request):
    context = {'form': None, 'result': None}

    if request.method == 'POST':
        form = TaxForm(request.POST)
        if form.is_valid():
            zakladni_mzda = form.cleaned_data['zakladni_mzda']
            prirazky = form.cleaned_data.get('prirazky', 0)

            # Výpočet hrubé mzdy
            hruba_mzda = zakladni_mzda + prirazky

            # Pojištění placené zaměstnavatelem (pro výpočet superhrubé mzdy)
            socialni_pojisteni_zamestnavatelem = math.ceil(hruba_mzda * 0.248)
            zdravotni_pojisteni_zamestnavatelem = math.ceil(hruba_mzda * 0.09)  # Zaokrouhleno nahoru

            # Superhrubá mzda
            nezaokrouhlena_superhruba_mzda = hruba_mzda + socialni_pojisteni_zamestnavatelem + zdravotni_pojisteni_zamestnavatelem
            superhruba_mzda = math.ceil(nezaokrouhlena_superhruba_mzda / 100.0) * 100

            # Pojištění placené zaměstnancem
            zdravotni_pojisteni = math.ceil(hruba_mzda * 0.045)  # Zaokrouhleno nahoru
            socialni_pojisteni = math.ceil(hruba_mzda * 0.071)  # Zaokrouhleno nahoru

            slevy_hodnoty = {
                'poplatnik': 2570,
                'prvni_dite': 1267,
                'druhe_dite': 1860,
                'treti_dite': 2320,
                'invalidita1_2': 210,
                'invalidita3': 420,
                'ztp_p': 1345,
                'pecujici_manžel': 2070,
                'ztp_p_pecujici': 4140,
                # Doplnit další slevy podle potřeby
            }

            # Výpočet celkové slevy na dani z příjmů
            total_deduction = 0
            for sleva in form.cleaned_data['slevy']:  # Iterace přes vybrané slevy
                total_deduction += slevy_hodnoty.get(sleva, 0)

            # Výpočet daně před slevami
            tax_rate = 0.23 if zakladni_mzda >= 131901 else 0.15
            pred_slevami_dan = superhruba_mzda * tax_rate

            # Daň po odečtení slev
            dan_po_slevach = pred_slevami_dan - total_deduction

            # Úprava čisté mzdy v závislosti na výsledku daně
            cista_mzda = hruba_mzda - zdravotni_pojisteni - socialni_pojisteni - dan_po_slevach

            # Save the result if the user is logged in
            if request.user.is_authenticated:
                CalculationResult.objects.create(
                    user=request.user,
                    hruba_mzda=hruba_mzda,
                    superhruba_mzda=superhruba_mzda,
                    zdravotni_pojisteni=zdravotni_pojisteni,
                    socialni_pojisteni=socialni_pojisteni,
                    dan_pred_slevami=pred_slevami_dan,
                    dan_po_slevach=dan_po_slevach,
                    cista_mzda=cista_mzda
                )

            context['form'] = form
            context['result'] = {
                'hruba_mzda': hruba_mzda,
                'superhruba_mzda': superhruba_mzda,
                'zdravotni_pojisteni': zdravotni_pojisteni,
                'socialni_pojisteni': socialni_pojisteni,
                'socialni_pojisteni_zamestnavatelem': socialni_pojisteni_zamestnavatelem,
                'zdravotni_pojisteni_zamestnavatelem': zdravotni_pojisteni_zamestnavatelem,
                'dan': pred_slevami_dan,
                'dan2': dan_po_slevach,
                'cista_mzda': cista_mzda,
            }

    else:
        form = TaxForm()
        context['form'] = form

    return render(request, 'calculate_tax.html', context)

def calculate_tax_rok(request):
    context = {'form': None, 'result': None}

    if request.method == 'POST':
        form = TaxFormRok(request.POST)
        if form.is_valid():
            zakladni_mzda = form.cleaned_data['zakladni_mzda1']


            # Výpočet hrubé mzdy
            hruba_mzda = zakladni_mzda

            # Pojištění placené zaměstnavatelem (pro výpočet superhrubé mzdy)
            socialni_pojisteni_zamestnavatelem = math.ceil(hruba_mzda * 0.248)
            zdravotni_pojisteni_zamestnavatelem = math.ceil(hruba_mzda * 0.09)  # Zaokrouhleno nahoru

            # Superhrubá mzda
            nezaokrouhlena_superhruba_mzda = hruba_mzda + socialni_pojisteni_zamestnavatelem + zdravotni_pojisteni_zamestnavatelem

            # Zaokrouhlení superhrubé mzdy nahoru na nejbližší stovku
            superhruba_mzda = math.ceil(nezaokrouhlena_superhruba_mzda / 100.0) * 100

            # Pojištění placené zaměstnancem
            zdravotni_pojisteni = math.ceil(hruba_mzda * 0.045)  # Zaokrouhleno nahoru
            socialni_pojisteni = math.ceil(hruba_mzda * 0.071)  # Zaokrouhleno nahoru

            # Předpokládáme, že v TaxForm existují pole jako BooleanField pro každou slevu
            # a zde jsou jejich hodnoty
            slevy_hodnoty = {
                'poplatnik': 30840,
                'prvni_dite': 15204,
                'druhe_dite': 22320,
                'treti_dite': 27840,
                'invalidita1_2': 2520,
                'invalidita3': 5040,
                'ztp_p': 16140,
                'pecujici_manžel': 24840,
                'ztp_p_pecujici': 49680,
                # Doplnit další slevy podle potřeby
            }

            # Výpočet celkové slevy na dani z příjmů
            total_deduction = 0
            selected_slevy = form.cleaned_data.get('slevy1', [])  # Seznam vybraných slev
            for sleva in selected_slevy:  # Iterace přes vybrané slevy
                total_deduction += slevy_hodnoty.get(sleva, 0)


            if zakladni_mzda >= 1582812:
                tax_rate = 0.23
            else:
                tax_rate = 0.15

            # Výpočet daně před slevami
            pred_slevami_dan = superhruba_mzda * tax_rate

            # Daň po odečtení slev
            dan_po_slevach = pred_slevami_dan - total_deduction

            # Úprava čisté mzdy v závislosti na výsledku daně
            cista_mzda = hruba_mzda - zdravotni_pojisteni - socialni_pojisteni - dan_po_slevach

            # Save the result if the user is logged in
            if request.user.is_authenticated:
                CalculationResultYear.objects.create(
                    user=request.user,
                    hruba_mzda=hruba_mzda,
                    superhruba_mzda=superhruba_mzda,
                    zdravotni_pojisteni=zdravotni_pojisteni,
                    socialni_pojisteni=socialni_pojisteni,
                    dan_pred_slevami=pred_slevami_dan,
                    dan_po_slevach=dan_po_slevach,
                    cista_mzda=cista_mzda
                )

            context['form'] = form
            context['result'] = {
                'hruba_mzda': hruba_mzda,
                'superhruba_mzda': superhruba_mzda,
                'zdravotni_pojisteni': zdravotni_pojisteni,
                'socialni_pojisteni': socialni_pojisteni,
                'socialni_pojisteni_zamestnavatelem': socialni_pojisteni_zamestnavatelem,
                'zdravotni_pojisteni_zamestnavatelem': zdravotni_pojisteni_zamestnavatelem,
                'dan': pred_slevami_dan,
                'dan2': dan_po_slevach,
                'cista_mzda': cista_mzda,
            }
    else:
        form = TaxFormRok()
        context['form'] = form

    return render(request, 'calculate_tax_rok.html', context)


def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Registration was successful.")
            return redirect("login")

    else:
        form = UserCreationForm()
    return render(request, "registration/registration.html", {"form": form})

@login_required
def history(request):
    form = HistoryFilterForm(request.GET)

    # Start with all results for the logged-in user
    monthly_results = CalculationResult.objects.filter(user=request.user)
    yearly_results = CalculationResultYear.objects.filter(user=request.user)

    if form.is_valid():
        sort_by = form.cleaned_data['sort_by']
        search_date = form.cleaned_data['search_date']

        # Adjust sorting based on the form input
        if sort_by == 'date':
            monthly_results = monthly_results.order_by('-created_at')
            yearly_results = yearly_results.order_by('-created_at')
        elif sort_by == 'gross_income':
            monthly_results = monthly_results.order_by('-hruba_mzda')
            yearly_results = yearly_results.order_by('-hruba_mzda')
        elif sort_by == 'net_income':
            monthly_results = monthly_results.order_by('-cista_mzda')
            yearly_results = yearly_results.order_by('-cista_mzda')

        # Filter by date if a date is provided
        if search_date:
            monthly_results = monthly_results.filter(created_at__date=search_date)
            yearly_results = yearly_results.filter(created_at__date=search_date)

    return render(request, 'history_user.html', {
        'form': form,
        'monthly_results': monthly_results,
        'yearly_results': yearly_results
    })
