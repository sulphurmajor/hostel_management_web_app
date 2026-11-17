from django.forms import ModelForm
from hostel.models import Student, Hostel, Payments, Warden, room, Visitor

class StudentForm (ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


class HostelForm(ModelForm):
    class Meta:
        model = Hostel
        fields = "__all__"

class PaymentForm(ModelForm):
    class Meta:
        model = Payments
        fields = ("student", "amount", "make_payment", "reason")

class WardenForm(ModelForm):
    class Meta:
        model = Warden
        fields = "__all__"

class RoomForm(ModelForm):
    class Meta:
        model = room
        fields = "__all__"


class VisitorForm(ModelForm):
    class Meta:
        model = Visitor
        fields = ("visitor_name", "phone_number", "student", "purpose")

