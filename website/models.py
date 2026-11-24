from django.db import models


class ToolSignup(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "free tools signup"
        verbose_name_plural = "free tools signups"

    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class CoachingRequest(models.Model):
    class Topic(models.TextChoices):
        PRICING = "Pricing and profit", "Pricing and profit"
        CLIENTS = "Getting more clients", "Getting more clients"
        SALON = "Opening or running a salon", "Opening or running a salon"
        OTHER = "Something else", "Something else"

    name = models.CharField(max_length=120)
    email = models.EmailField()
    topic = models.CharField(max_length=40, choices=Topic.choices)
    message = models.TextField(blank=True, max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.topic}"
