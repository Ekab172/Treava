from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import CoachingRequestForm, ToolSignupForm
from .models import ToolSignup


@require_http_methods(["GET", "POST"])
def home(request):
    lead_form = ToolSignupForm()
    contact_form = CoachingRequestForm()
    status = 200

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "lead":
            lead_form = ToolSignupForm(request.POST)
            if lead_form.is_valid():
                _, created = ToolSignup.objects.get_or_create(
                    email=lead_form.cleaned_data["email"]
                )
                if created:
                    messages.success(
                        request,
                        "Thank you. Your free tools signup has been saved.",
                        extra_tags="lead",
                    )
                else:
                    messages.success(
                        request,
                        "This email is already registered for the free tools.",
                        extra_tags="lead",
                    )
                return redirect(reverse("website:home") + "#free")
        elif form_type == "contact":
            contact_form = CoachingRequestForm(request.POST)
            if contact_form.is_valid():
                contact_form.save()
                messages.success(
                    request,
                    "Thank you. Your coaching request has been saved for Treava’s team.",
                    extra_tags="contact",
                )
                return redirect(reverse("website:home") + "#contact")
        else:
            messages.error(request, "Please submit one of the forms below.")
            status = 400

    return render(
        request,
        "website/home.html",
        {"lead_form": lead_form, "contact_form": contact_form},
        status=status,
    )
