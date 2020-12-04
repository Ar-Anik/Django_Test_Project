from django.contrib import admin
from .models import Product
from .models import Cart
from .models import Order
from .models import Review
from .models import FAQ

# Register your models here.

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Review)

class FAQadmin(admin.ModelAdmin):
    list_display = ['ordernumber', 'question', 'status', 'created_at', 'updated_at']

admin.site.register(FAQ, FAQadmin)

