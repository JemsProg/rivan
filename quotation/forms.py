from django import forms

class TrainingQuotationForm(forms.Form):
    COURSE_CHOICES = [
        ("RivanIT CCNA Network Engineer Training 200-301", "RivanIT CCNA Network Engineer Training 200-301"),
        ("CCNP Enterprise: ENCORxENARSIxSDWAN", "CCNP Enterprise: ENCORxENARSIxSDWAN"),
        ("COMPTIA SECURITY PLUS+", "COMPTIA SECURITY PLUS+"),
        ("COMPTIA SEC+ 701 (EXAM) Voucher", "COMPTIA SEC+ 701 (EXAM) Voucher"),
        ("RIVAN ITILV3/4", "RIVAN ITILV3/4"),
    ]

    FUNDING_CHOICES = [
        ("Personal/Individual", "Personal/Individual"),
        ("Sponsor/Corporate", "Sponsor/Corporate"),
    ]

    EXAM_VOUCHER_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
    ]

    customer_name = forms.CharField(
        max_length=255, 
        required=True, 
        label="Customer/Company Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter customer or company name"})
    )
    course = forms.ChoiceField(
        choices=COURSE_CHOICES, 
        required=True, 
        label="Course for Quotation",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    training_location = forms.CharField(
        initial="Makati", 
        required=True, 
        label="Training Location",
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"})
    )
    delivery_mode = forms.CharField(
        initial="Face-to-Face", 
        required=True, 
        label="Delivery Mode",
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"})
    )
    number_of_attendees = forms.IntegerField(
        min_value=1, 
        required=True, 
        label="Number of Attendees",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    funding = forms.ChoiceField(
        choices=FUNDING_CHOICES, 
        required=True, 
        label="Choose Funding",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    voucher = forms.ChoiceField(
        choices=EXAM_VOUCHER_CHOICES, 
        required=True, 
        label="Would you like to avail a voucher for the exam?",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    job_title = forms.CharField(
        max_length=255, 
        required=False, 
        label="Job Title",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your job title"})
    )
    email = forms.EmailField(
        required=True, 
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"})
    )
    contact_number = forms.CharField(
        max_length=15, 
        required=True, 
        label="Contact Number",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your contact number"})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Enter your message (optional)"}),
        required=False, 
        label="Message"
    )
    not_a_robot = forms.BooleanField(
        required=True, 
        label="I'm not a robot",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
