from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class SEOFields(models.Model):
    """
    Abstract mixin that gives any model reusable, optional SEO overrides.
    If left blank, views/templates fall back to sensible generated defaults
    (see core/context_processors.py and templates/core/base.html).
    """
    meta_title = models.CharField(
        max_length=70, blank=True,
        help_text="Overrides the <title> tag. Leave blank to auto-generate. Aim for 50-60 characters.",
    )
    meta_description = models.CharField(
        max_length=160, blank=True,
        help_text="Search-result snippet. Leave blank to auto-generate. Aim for 120-160 characters.",
    )
    meta_keywords = models.CharField(
        max_length=255, blank=True,
        help_text="Optional, comma-separated. Modern search engines mostly ignore this, kept for completeness.",
    )

    class Meta:
        abstract = True


class ResourceCategory(models.TextChoices):
    EDUCATION = "education", "Education"
    WELLNESS = "wellness", "Wellness"
    SUPPORT = "support", "Support"
    VOLUNTEER = "volunteer", "Volunteer"


class Resource(models.Model):
    """A 'Find a Path' card / resource pointer shown on the Resources page and home page."""
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=ResourceCategory.choices)
    emoji = models.CharField(max_length=8, blank=True, help_text="Small emoji shown next to the title, e.g. 🎓")
    summary = models.CharField(max_length=200, help_text="One-line description shown on cards.")
    body = models.TextField(blank=True, help_text="Optional longer detail shown on the Resources page.")
    external_link = models.URLField(blank=True, help_text="Optional link to an external resource.")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class WorkEntry(SEOFields):
    """A single logged activity/session for the 'Work Done Till Date' timeline."""
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    date = models.DateField(help_text="Date the activity took place.")
    location = models.CharField(max_length=150, blank=True)
    summary = models.CharField(max_length=220, help_text="Short teaser shown on the timeline list.")
    body = models.TextField(help_text="Full write-up shown on the detail page.")
    cover_image = models.ImageField(upload_to="work/", blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name = "Work entry"
        verbose_name_plural = "Work entries"

    def __str__(self):
        return f"{self.title} ({self.date})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:170]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:work_detail", kwargs={"slug": self.slug})


class SunshineEntry(models.Model):
    """
    A single 'Today's Sunshine' entry: a quote plus its meaning, a reminder and an
    affirmation. The view picks the entry matching today's date if one exists,
    otherwise falls back to the most recently published one, so the page always
    has something to show without needing a new entry every single day.
    """
    date = models.DateField(unique=True, help_text="The date this entry is meant for.")
    quote = models.CharField(max_length=300)
    meaning = models.TextField(help_text="What the quote means, in plain language.")
    reminder = models.CharField(max_length=200, help_text="A short, actionable reminder for today.")
    affirmation = models.CharField(max_length=200)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Sunshine entry"
        verbose_name_plural = "Sunshine entries"

    def __str__(self):
        return f"Sunshine — {self.date}"


class ContactMessage(models.Model):
    """Stores messages submitted through the Contact page form."""
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}> — {self.created_at:%Y-%m-%d}"
