from django.contrib import admin
from .models import MarketingPreference
# Register your models here.

class MarketingPreferenceAdmin(admin.ModelAdmin):
    list_display = ['__str__','subscribed','updated']    # the view we get after entering the admin and clicking on the marketingpreference
    readonly_fields = ['mailchimp_subscribed','timestamp','updated']
    class Meta :
        model = MarketingPreference
        fields = ['user','subscribed','mailchmp_msg','mailchimp_subscribed','timestamp','updated']

admin.site.register(MarketingPreference,MarketingPreferenceAdmin)

