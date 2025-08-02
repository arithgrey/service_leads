from django.db import models

class LeadMetrics(models.Model):
    """
    Modelo para almacenar métricas pre-calculadas de leads
    """
    date = models.DateField()
    total_leads = models.IntegerField(default=0)
    new_leads = models.IntegerField(default=0)
    pending_leads = models.IntegerField(default=0)
    contacted_leads = models.IntegerField(default=0)
    discarded_leads = models.IntegerField(default=0)
    process_leads = models.IntegerField(default=0)
    converted_leads = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['date']
        ordering = ['-date']
    
    def __str__(self):
        return f"Métricas del {self.date}" 