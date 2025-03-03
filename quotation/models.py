from django.db import models

class TrainingQuotationRequest(models.Model):
    COURSE_CHOICES = [
        ("CCNA", "CCNA"),
        ("CCNP", "CCNP"),
        ("CompTIA Security+", "CompTIA Security+"),
        ("ITIL", "ITIL"),
    ]
    
    LOCATION_CHOICES = [
        ("Makati", "Makati"),
    ]
    
    DELIVERY_MODE_CHOICES = [
        ("F2F", "Face-to-Face"),
    ]
    
    FUNDING_CHOICES = [
        ("Personal/Individual", "Personal/Individual"),
        ("Sponsor/Corporate", "Sponsor/Corporate"),
    ]
    
    VOUCHER_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
    ]
    
    course = models.CharField(max_length=50, choices=COURSE_CHOICES)
    training_location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    delivery_mode = models.CharField(max_length=50, choices=DELIVERY_MODE_CHOICES)
    number_of_attendees = models.PositiveIntegerField()
    funding = models.CharField(max_length=50, choices=FUNDING_CHOICES)
    voucher = models.CharField(max_length=3, choices=VOUCHER_CHOICES)
    full_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    message = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.course}"
