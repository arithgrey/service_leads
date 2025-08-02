from django.contrib import admin
from lead_metrics.models import LeadMetrics

@admin.register(LeadMetrics)
class LeadMetricsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_leads', 'new_leads', 'converted_leads', 'conversion_rate']
    list_filter = ['date']
    readonly_fields = ['date', 'total_leads', 'new_leads', 'pending_leads', 'contacted_leads', 
                      'discarded_leads', 'process_leads', 'converted_leads']
    
    def conversion_rate(self, obj):
        if obj.total_leads > 0:
            return f"{(obj.converted_leads / obj.total_leads * 100):.2f}%"
        return "0%"
    conversion_rate.short_description = 'Tasa de Conversión' 