from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import mail_admins
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .forms import ContactForm,SunshineEntryForm,WorkEntryForm
from .models import Resource, SunshineEntry, WorkEntry,ContactMessage


def home(request):
    """Landing page: mission teaser, resource cards, latest work entries."""
    resources = Resource.objects.filter(is_published=True)[:4]
    latest_work = WorkEntry.objects.filter(is_published=True)[:3]
    context = {
        "resources": resources,
        "latest_work": latest_work,
        "meta_title": "Nayi Raah — Turning Ideas Into Skills, Support Into Action",
        "meta_description": (
            "Nayi Raah supports girls across India with education, wellness "
            "guidance and a safe space to grow with confidence and courage."
        ),
    }
    return render(request, "core/home.html", context)


def about(request):
    context = {
        "meta_title": "About Nayi Raah — Our Mission",
        "meta_description": (
            "Learn about Nayi Raah's mission to give every girl access to "
            "support, education and encouragement to bloom with confidence."
        ),
    }
    return render(request, "core/about.html", context)


def resources(request):
    """Resources page grouped by category for the 'Find a Path' section."""
    resource_qs = Resource.objects.filter(is_published=True)
    grouped = {}
    for resource in resource_qs:
        grouped.setdefault(resource.category, []).append(resource)
    context = {
        "grouped_resources": grouped,
        "meta_title": "Resources — Education, Wellness, Support & Volunteering",
        "meta_description": (
            "Explore Nayi Raah's resources on education, wellness, support "
            "and volunteering, curated to help every girl find her path."
        ),
    }
    return render(request, "core/resources.html", context)


def sunshine(request):
    """Today's Sunshine: picks today's entry if published, else the latest one."""
    today = timezone.localdate()
    entry = SunshineEntry.objects.filter(date=today, is_published=True).first()
    if entry is None:
        entry = SunshineEntry.objects.filter(is_published=True).first()
    context = {
        "entry": entry,
        "meta_title": "Today's Sunshine — Daily Reminder & Affirmation",
        "meta_description": (
            "A daily quote, reminder and affirmation from Nayi Raah to help "
            "you grow one step at a time."
        ),
    }
    return render(request, "core/sunshine.html", context)


def work_list(request):
    """Chronological 'Work Done Till Date' timeline."""
    entries = WorkEntry.objects.filter(is_published=True)
    context = {
        "entries": entries,
        "meta_title": "Our Work — Sessions & Activities by Nayi Raah",
        "meta_description": (
            "A timeline of the sessions, talks and activities Nayi Raah has "
            "carried out so far, in its own words."
        ),
    }
    return render(request, "core/work_list.html", context)


def work_detail(request, slug):
    entry = get_object_or_404(WorkEntry, slug=slug, is_published=True)
    context = {
        "entry": entry,
        "meta_title": entry.meta_title or f"{entry.title} — Nayi Raah",
        "meta_description": entry.meta_description or entry.summary,
    }
    return render(request, "core/work_detail.html", context)


@require_http_methods(["GET", "POST"])
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            # Best-effort notification; console backend in dev, real SMTP in prod
            # (see settings.py). Failure here should never break the user's
            # experience of having successfully sent their message.
            try:
                mail_admins(
                    subject=f"New contact message from {contact_message.name}",
                    message=contact_message.message,
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, "Thank you — your message has been sent. We'll get back to you soon.")
            return redirect(reverse("core:contact"))
    else:
        form = ContactForm()

    context = {
        "form": form,
        "meta_title": "Contact Nayi Raah",
        "meta_description": "Reach out to Nayi Raah for guidance, support or to get involved.",
    }
    return render(request, "core/contact.html", context)


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {request.scheme}://{request.get_host()}{reverse('sitemap')}",
    ]
    return TemplateResponse(request, "core/robots.txt", {"lines": lines}, content_type="text/plain")

@staff_member_required
def contact_admin(request):
    messages = ContactMessage.objects.all()
    return render( request, "core/contact_admin.html", { "messages": messages, }, )

@staff_member_required
def sunshine_admin(request):
    entries = SunshineEntry.objects.all()

    if request.method == "POST":
        form = SunshineEntryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Sunshine entry added successfully."
            )
            return redirect("core:sunshine_admin")
    else:
        form = SunshineEntryForm()

    return render(
        request,
        "core/sunshine_admin.html",
        {
            "entries": entries,
            "form": form,
        },
    )

@staff_member_required
def work_admin(request):
    entries = WorkEntry.objects.all()

    if request.method == "POST":
        form = WorkEntryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Work entry added successfully."
            )
            return redirect("core:work_admin")
    else:
        form = WorkEntryForm()

    return render(
        request,
        "core/work_admin.html",
        {
            "entries": entries,
            "form": form,
        },
    )

def custom_404(request, exception=None):
    return render(request, "core/404.html", status=404)
