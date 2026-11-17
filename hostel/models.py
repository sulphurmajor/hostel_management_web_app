from django.db import models

# Create your models here.

class Student(models.Model):

    GENDER_CHOICES = [
        ("M","Male"),
        ("F","Female"),
        ("O","Other")
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    birth_date = models.DateField(auto_now=False)
    no_of_courses = models.IntegerField(default=0)
    gender = models.CharField(choices = GENDER_CHOICES, max_length=1,default="M")
    hostel = models.ForeignKey("Hostel", on_delete=models.CASCADE, related_name="students",default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Hostel(models.Model):
    
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=500)
    total_rooms = models.IntegerField(default=0)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Warden(models.Model):
    GENDER_CHOICES = [
                ("M","Male"),
                ("F","Female"),
                ("O","Other")
            ]
    first_name = models.CharField(max_length =100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(choices = GENDER_CHOICES, max_length =1,default="M" )
    hostel = models.ForeignKey(Hostel, on_delete = models.CASCADE, related_name = "Warden",default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class room(models.Model):
    STATUS_CHOICES = [
        ("O","Occupied"),
        ("A","Available"),
        ("M","Maintenance")
    ]
    room_number = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    hostel = models.ForeignKey(Hostel, on_delete = models.CASCADE,related_name = "rooms", default=None,null = True,blank = True)
    status = models.CharField(choices = STATUS_CHOICES, max_length=1,default ="A")

    def __str__(self):
        return f"Room {self.room_number}"


class Payments(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE,
                                related_name = "payments",default = None, null = True, blank = True)
    make_payment = models.BooleanField(default =False)
    amount = models.DecimalField(max_digits = 10,decimal_places = 2,
                                 default =0.00)
    date =models.DateTimeField(auto_now_add = True)
    reason = models.TextField(max_length = 500,default = "Payment for hostel fees")

    def __str__(self):
        return f"Payment {self.pk}: {self.amount}"


class Visitor(models.Model):
    visitor_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=30)
    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        related_name="visitors",
        null=True,
        blank=True,
    )
    purpose = models.TextField(max_length=500)
    visit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.visitor_name