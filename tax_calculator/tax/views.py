import math

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import TaxForm, TaxFormRok,HistoryFilterForm, SignupForm

from .models import CalculationResult, CalculationResultYear


def index(request):
    return render(request, "index.html")

def novinky(request):
    return render(request, "novinky.html")

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
                'ztp_p': 1345,
                # Doplnit další slevy podle potřeby
            }

            deti_hodnoty = {
                'bezdětný': 0,
                'prvni_dite': 1267,
                'druhe_dite': 1860,
                'treti_dite': 2320,
            }

            invalidita_hodnoty = {
                'bezinvalidity': 0,
                'invalidita1_2': 210,
                'invalidita3': 420,
            }

            ztp_hodnoty = {
                'bez': 0,
                'pecujici_manžel': 2070,
                'ztp_p_pecujici': 4140,
            }

            total_deduction = 0

# Ensure both slevy and deti are lists before concatenating
            slevy_list = form.cleaned_data['slevy'] if isinstance(form.cleaned_data['slevy'], list) else [form.cleaned_data['slevy']]
            deti_list = form.cleaned_data['deti'] if isinstance(form.cleaned_data['deti'], list) else [form.cleaned_data['deti']]
            invalidita_list = form.cleaned_data['invalidita'] if isinstance(form.cleaned_data['invalidita'], list) else [form.cleaned_data['invalidita']]
            ztp_list = form.cleaned_data['ztp'] if isinstance(form.cleaned_data['ztp'], list) else [form.cleaned_data['ztp']]

# Spojení seznamů slev a dětských slev
            all_slevy = slevy_list + deti_list + invalidita_list + ztp_list

# Iterace přes všechny vybrané slevy a slevy na děti
            for sleva in all_slevy:
                total_deduction += slevy_hodnoty.get(sleva, 0) + deti_hodnoty.get(sleva, 0) + invalidita_hodnoty.get(sleva, 0) + ztp_hodnoty.get(sleva, 0)

            # Výpočet daně před slevami
            tax_rate = 0.23 if zakladni_mzda >= 131901 else 0.15
            pred_slevami_dan = superhruba_mzda * tax_rate

            # Daň po odečtení slev
            dan_po_slevach = pred_slevami_dan - total_deduction

            # Úprava čisté mzdy v závislosti na výsledku daně
            cista_mzda = hruba_mzda - zdravotni_pojisteni - socialni_pojisteni - dan_po_slevach

            slevy_labels = {
                'poplatnik': 'Základní sleva na poplatníka',
                'ztp_p': 'Sleva na držitele průkazu ZTP/P',
                # doplnit další
            }

            deti_labels = {
                'bezdětný': 'Žádná možnost',
                'prvni_dite': 'Sleva na jedno dítě',
                'druhe_dite': 'Sleva na dvě děti',
                'treti_dite': 'Sleva na tři a více děti',
                # doplnit další
            }

            invalidita_labels = {
                'bezinvalidity': 'Žádná možnost',
                'invalidita1_2': 'Sleva na invaliditu 1. a 2. stupně',
                'invalidita3': 'Sleva na invaliditu 3. stupně',
                # doplnit další
            }

            ztp_labels = {
                'bez': 'Žádná možnost',
                'pecujici_manžel': 'Sleva na manželku ZTP/P pečující o dítě do 3 let s příjmem nepřesahujícím 68 000 Kč ročně',
                'ztp_p_pecujici': 'Sleva na manžela ZTP/P pečující o dítě do 3 let s příjmem nepřesahujícím 68 000 Kč ročně',
                 # doplnit další
            }

            pouzite_slevy_list = [
                f"{slevy_labels[key]}: {slevy_hodnoty[key]} Kč" for key in slevy_list if key in slevy_hodnoty and slevy_hodnoty[key] > 0
            ] + [
                f"{deti_labels[key]}: {deti_hodnoty[key]} Kč" for key in deti_list if key in deti_hodnoty and deti_hodnoty[key] > 0
            ] + [
                f"{invalidita_labels[key]}: {invalidita_hodnoty[key]} Kč" for key in invalidita_list if key in invalidita_hodnoty and invalidita_hodnoty[key] > 0
            ] + [
                f"{ztp_labels[key]}: {ztp_hodnoty[key]} Kč" for key in ztp_list if key in ztp_hodnoty and ztp_hodnoty[key] > 0
            ]

            pouzite_slevy = ', '.join(pouzite_slevy_list)

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
                    cista_mzda=cista_mzda,
                    pouzite_slevy=pouzite_slevy
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
                'pouzite_slevy': pouzite_slevy,
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
                'ztp_p': 16140,
                # Doplnit další slevy podle potřeby
            }

            deti_hodnoty = {
                'bezdětný': 0,
                'prvni_dite': 15204,
                'druhe_dite': 22320,
                'treti_dite': 27840,
            }

            invalidita_hodnoty = {
                'bezinvalidity': 0,
                'invalidita1_2': 2520,
                'invalidita3': 5040,
            }

            ztp_hodnoty = {
                'bez': 0,
                'pecujici_manžel': 24840,
                'ztp_p_pecujici': 49680,
            }

            total_deduction = 0

        # Ensure both slevy and deti are lists before concatenating
            slevy_list = form.cleaned_data['slevy1'] if isinstance(form.cleaned_data['slevy1'], list) else [form.cleaned_data['slevy1']]
            deti_list = form.cleaned_data['deti1'] if isinstance(form.cleaned_data['deti1'], list) else [form.cleaned_data['deti1']]
            invalidita_list = form.cleaned_data['invalidita1'] if isinstance(form.cleaned_data['invalidita1'], list) else [form.cleaned_data['invalidita1']]
            ztp_list = form.cleaned_data['ztp1'] if isinstance(form.cleaned_data['ztp1'], list) else [form.cleaned_data['ztp1']]

        # Spojení seznamů slev a dětských slev
            all_slevy = slevy_list + deti_list + invalidita_list + ztp_list

        # Iterace přes všechny vybrané slevy a slevy na děti
            for sleva in all_slevy:
                total_deduction += slevy_hodnoty.get(sleva, 0) + deti_hodnoty.get(sleva, 0) + invalidita_hodnoty.get(sleva, 0) + ztp_hodnoty.get(sleva, 0)

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

            slevy_labels = {
                'poplatnik': 'Základní sleva na poplatníka',
                'ztp_p': 'Sleva na držitele průkazu ZTP/P',
                # doplnit další
            }

            deti_labels = {
                'bezdětný': 'Žádná možnost',
                'prvni_dite': 'Sleva na jedno dítě',
                'druhe_dite': 'Sleva na dvě děti',
                'treti_dite': 'Sleva na tři a více děti',
                # doplnit další
            }

            invalidita_labels = {
                'bezinvalidity': 'Žádná možnost',
                'invalidita1_2': 'Sleva na invaliditu 1. a 2. stupně',
                'invalidita3': 'Sleva na invaliditu 3. stupně',
                # doplnit další
            }

            ztp_labels = {
                'bez': 'Žádná možnost',
                'pecujici_manžel': 'Sleva na manželku ZTP/P pečující o dítě do 3 let s příjmem nepřesahujícím 68 000 Kč ročně',
                'ztp_p_pecujici': 'Sleva na manžela ZTP/P pečující o dítě do 3 let s příjmem nepřesahujícím 68 000 Kč ročně',
                # doplnit další
            }

            pouzite_slevy_list = [
                f"{slevy_labels[key]}: {slevy_hodnoty[key]} Kč" for key in slevy_list if key in slevy_hodnoty and slevy_hodnoty[key] > 0
            ] + [
                f"{deti_labels[key]}: {deti_hodnoty[key]} Kč" for key in deti_list if key in deti_hodnoty and deti_hodnoty[key] > 0
            ] + [
                f"{invalidita_labels[key]}: {invalidita_hodnoty[key]} Kč" for key in invalidita_list if key in invalidita_hodnoty and invalidita_hodnoty[key] > 0
            ] + [
                f"{ztp_labels[key]}: {ztp_hodnoty[key]} Kč" for key in ztp_list if key in ztp_hodnoty and ztp_hodnoty[key] > 0
            ]

            pouzite_slevy = ', '.join(pouzite_slevy_list)

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
                    cista_mzda=cista_mzda,
                    pouzite_slevy=pouzite_slevy
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
                'pouzite_slevy': pouzite_slevy,
            }
    else:
        form = TaxFormRok()
        context['form'] = form

    return render(request, 'calculate_tax_rok.html', context)


def registration(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "REGISTRACE PROBĚHLA ÚSPĚŠNĚ!")
            return redirect("login")

    else:
        form = SignupForm()
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

@login_required
def delete_monthly_result(request, result_id):
    result = CalculationResult.objects.get(pk=result_id, user=request.user)  # Ensure user owns the result
    result.delete()
    messages.success(request, "MĚSÍČNÍ VÝPOČET BYL ÚSPĚŠNĚ ODSTRANĚN Z HISTORIE!")
    return redirect('result_history')  # Assumes 'history' is the name of your history view

@login_required
def delete_yearly_result(request, result_id):
    result = CalculationResultYear.objects.get(pk=result_id, user=request.user)  # Ensure user owns the result
    result.delete()
    messages.success(request, "ROČNÍ VÝPOČET BYL ÚSPĚŠNĚ ODSTRANĚN Z HISTORIE!")
    return redirect('result_history')