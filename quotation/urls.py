from django.urls import path
from .views import quotation_quote

urlpatterns = [
    path("request-quotation/", quotation_quote, name="quotation_quote"),
]
