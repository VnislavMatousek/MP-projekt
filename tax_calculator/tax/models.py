from django.db import models
from django.contrib.auth.models import User

class CalculationResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hruba_mzda = models.FloatField()
    superhruba_mzda = models.FloatField()
    zdravotni_pojisteni = models.FloatField()
    socialni_pojisteni = models.FloatField()
    dan_pred_slevami = models.FloatField()
    dan_po_slevach = models.FloatField()
    cista_mzda = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    pouzite_slevy = models.TextField(default="", blank=True)

    def __str__(self):
        return f"Result for {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"


class CalculationResultYear(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hruba_mzda = models.FloatField()
    superhruba_mzda = models.FloatField()
    zdravotni_pojisteni = models.FloatField()
    socialni_pojisteni = models.FloatField()
    dan_pred_slevami = models.FloatField()
    dan_po_slevach = models.FloatField()
    cista_mzda = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    pouzite_slevy = models.TextField(default="", blank=True)

    def __str__(self):
        return f"Result for {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"