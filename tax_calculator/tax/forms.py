from django.forms import ModelForm
from django import forms


class TaxForm(forms.Form):
    SLAVY_CHOICES = [
        ('poplatnik', 'Sleva na poplatníka'),
        ('prvni_dite', 'Sleva na první dítě'),
        ('druhe_dite', 'Sleva na druhé dítě'),
        ('treti_dite', 'Sleva na třetí a další dítě'),
        ('invalidita1_2', 'Sleva na invaliditu 1. a 2. stupně'),
        ('invalidita3', 'Sleva na invaliditu 3. stupně'),
        ('ztp_p', 'Slevu na držitele průkazu ZTP/P'),
        ('pecujici_manžel', 'Sleva na manžela/ku pečující o dítě do 3 let'),
        ('ztp_p_pecujici', 'Sleva na manžela ZTP/P pečující o dítě do 3 let'),
    ]
    zakladni_mzda = forms.IntegerField(label='Základní mzda')
    prirazky = forms.IntegerField(label='Příplatky za víkend, noc a přesčas', required=False, initial=0)
    slevy = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=SLAVY_CHOICES,
        label='Slevy na dani'
    )

class TaxFormRok(forms.Form):
    SLEVY_CHOICES = [
        ('poplatnik', 'Sleva na poplatníka'),
        ('prvni_dite', 'Sleva na první dítě'),
        ('druhe_dite', 'Sleva na druhé dítě'),
        ('treti_dite', 'Sleva na třetí a další dítě'),
        ('invalidita1_2', 'Sleva na invaliditu 1. a 2. stupně'),
        ('invalidita3', 'Sleva na invaliditu 3. stupně'),
        ('ztp_p', 'Slevu na držitele průkazu ZTP/P'),
        ('pecujici_manžel', 'Sleva na manžela/ku pečující o dítě do 3 let'),
        ('ztp_p_pecujici', 'Sleva na manžela ZTP/P pečující o dítě do 3 let'),
    ]
    zakladni_mzda1 = forms.IntegerField(label='Celkové příjmy za rok')
    slevy1 = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=SLEVY_CHOICES,
        label='Slevy na dani'
    )

class HistoryFilterForm(forms.Form):
    DATE = 'date'
    GROSS_INCOME = 'gross_income'
    NET_INCOME = 'net_income'

    SORT_CHOICES = [
        (DATE, 'Date'),
        (GROSS_INCOME, 'Gross Income'),
        (NET_INCOME, 'Net Income'),
    ]

    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False)
    search_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))