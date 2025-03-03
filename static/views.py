import os
import openpyxl
import xmlrpc.client
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.http import HttpResponse
from ..static.forms import TrainingQuotationForm
from .models import TrainingQuotationRequest
from django.conf import settings
from django.http import JsonResponse

# Odoo connection details
ODOO_URL = 'https://rivanit.odoo.com/'
ODOO_DB = 'rivanit'
ODOO_USERNAME = 'rivaninstitute@gmail.com'
ODOO_PASSWORD = 'C1sc0123$$'

# Authenticate with Odoo
common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})

models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")


def create_odoo_customer(customer_name, email, phone):
    """Create or get a customer in Odoo."""
    customer = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD, 'res.partner', 'search_read',
        [[['name', '=', customer_name]]], {'fields': ['id']}
    )

    if customer:
        print(f"✅ Customer {customer_name} already exists with ID {customer[0]['id']}")
        return customer[0]['id']

    customer_id = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD, 'res.partner', 'create',
        [{'name': customer_name, 'email': email, 'phone': phone, 'customer_rank': 1}]
    )

    print(f"✅ Created new customer {customer_name} with ID {customer_id}")
    return customer_id


def create_odoo_product(course_name):
    """Create or get a product in Odoo."""
    product = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD, 'product.product', 'search_read',
        [[['name', '=', course_name]]], {'fields': ['id']}
    )

    if product:
        print(f"✅ Product {course_name} already exists with ID {product[0]['id']}")
        return product[0]['id']

    product_id = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD, 'product.product', 'create',
        [{'name': course_name, 'type': 'service'}]
    )

    print(f"✅ Created new product {course_name} with ID {product_id}")
    return product_id


def create_odoo_quotation(customer_id, product_id, data, full_names):
    """Create a new quotation in Odoo with attendees' names and quantity multiplied by the number of attendees."""
    num_attendees = int(data['number_of_attendees'])
    full_names_str = ", ".join(full_names) if full_names else "N/A"

    note = (
        f"📍 Training Location: {data['training_location']}\n"
        f"🎓 Delivery Mode: {data['delivery_mode']}\n"
        f"👥 Number of Attendees: {num_attendees}\n"
        f"💰 Funding: {data['funding']}\n"
        f"🎫 Voucher: {data['voucher']}\n"
        f"👨‍💼 Job Title: {data['job_title']}\n"
        f"📧 Email: {data['email']}\n"
        f"📞 Contact Number: {data['contact_number']}\n"
        f"📝 Message: {data['message']}\n"
        f"👤 Attendee Names: {full_names_str}\n"
    )

    quotation_id = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD, 'sale.order', 'create',
        [{
            'partner_id': customer_id,
            'order_line': [(0, 0, {'product_id': product_id, 'product_uom_qty': num_attendees})],  # Multiply by attendees
            'note': note,
        }]
    )

    print(f"✅ Created new quotation with ID {quotation_id}")
    return quotation_id


def quotation_quote(request):
    if request.method == "POST":
        form = TrainingQuotationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data.pop("not_a_robot", None)  # Remove unnecessary field

            customer_name = data["customer_name"]
            email = data["email"]
            phone = data["contact_number"]
            course_name = data["course"]
            full_names = request.POST.getlist("full_name[]")  # Get all attendees' names

            customer_id = create_odoo_customer(customer_name, email, phone)
            product_id = create_odoo_product(course_name)
            quotation_id = create_odoo_quotation(customer_id, product_id, data, full_names)

            return JsonResponse({"success": True, "quotation_id": quotation_id})

        return JsonResponse({"success": False, "errors": form.errors})
    
    return JsonResponse({"success": False, "error": "Invalid request"})
