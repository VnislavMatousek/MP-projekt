from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class TaxForm(forms.Form):
    SLAVY_CHOICES = [
        ('poplatnik', 'Základní sleva na poplatníka'),
        ('ztp_p', 'Sleva na držitele průkazu ZTP/P'),
    ]

    DETI_CHOICES = [
        ('bezdětný', 'Žádná možnost'),
        ('prvni_dite', 'Sleva na jedno dítě'),
        ('druhe_dite', 'Sleva na dvě děti'),
        ('treti_dite', 'Sleva na tři a více děti'),
    ]
    INVALIDITA_CHOICES = [
        ('bezinvalidity', 'Žádná možnost'),
        ('invalidita1_2', 'Sleva na invaliditu 1. a 2. stupně'),
        ('invalidita3', 'Sleva na invaliditu 3. stupně'),
    ]
    ZTP_CHOICES = [
        ('bez', 'Žádná možnost'),
        ('pecujici_manžel', 'Sleva na manželku ZTP/P pečující o dítě do 3 let s příjmem nepřesahujícím 68 000 Kč ročně'),
        ('ztp_p_pecujici', 'Sleva na manžela ZTP/P pečující o dítě do 3 let s příjmem nepřesahujícím 68 000 Kč ročně'),
    ]
    zakladni_mzda = forms.IntegerField(label='Základní mzda')
    prirazky = forms.IntegerField(label='Příplatky za víkend, noční směny nebo přesčasy', required=False, initial=0)
    slevy = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=SLAVY_CHOICES,
        label='Slevy na dani'
    )
    deti = forms.ChoiceField(choices=DETI_CHOICES, label='Slevy na děti')
    invalidita = forms.ChoiceField(choices=INVALIDITA_CHOICES, label='Sleva pro lidi s invalidy')
    ztp = forms.ChoiceField(choices=ZTP_CHOICES, label='Sleva pro partnera se ZTP/P průkazem')

class TaxFormRok(forms.Form):
    SLEVY_CHOICES = [
        ('poplatnik', 'Základní sleva na poplatníka'),
        ('ztp_p', 'Sleva na držitele průkazu ZTP/P'),
    ]

    DETI_CHOICES1 = [
        ('bezdětný', 'Žádná možnost'),
        ('prvni_dite', 'Sleva na jedno dítě'),
        ('druhe_dite', 'Sleva na dvě děti'),
        ('treti_dite', 'Sleva na tři a více dětí'),
    ]
    INVALIDITA_CHOICES1 = [
        ('bezinvalidity', 'Žádná možnost'),
        ('invalidita1_2', 'Sleva na invaliditu 1. a 2. stupně'),
        ('invalidita3', 'Sleva na invaliditu 3. stupně'),
    ]
    ZTP_CHOICES1 = [
        ('bez', 'Žádná možnost'),
        ('pecujici_manžel', 'Sleva na manželku ZTP/P pečující o dítě do 3 let s příjmem nepřesahujícím 68 000 Kč ročně'),
        ('ztp_p_pecujici', 'Sleva na manžela ZTP/P pečující o dítě do 3 let s příjmem nepřesahujícím 68 000 Kč ročně'),
    ]
    zakladni_mzda1 = forms.IntegerField(label='Celkové příjmy za rok')
    slevy1 = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=SLEVY_CHOICES,
        label='Slevy na dani'
    )
    deti1 = forms.ChoiceField(choices=DETI_CHOICES1, label='Slevy na děti')
    invalidita1 = forms.ChoiceField(choices=INVALIDITA_CHOICES1, label='Sleva pro lidi s invaliditou')
    ztp1 = forms.ChoiceField(choices=ZTP_CHOICES1, label='Sleva pro partnera se ZTP/P průkazem')

class HistoryFilterForm(forms.Form):
    DATE = 'date'
    GROSS_INCOME = 'gross_income'
    NET_INCOME = 'net_income'

    SORT_CHOICES = [
        (DATE, 'Datumu (vzestupně)'),
        (GROSS_INCOME, 'Hrubé mzdy (sestupně)'),
        (NET_INCOME, 'Čisté mzdy (sestupně)'),
    ]

    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, label='Seřadit podle:')
    search_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Vyhledat datum:")