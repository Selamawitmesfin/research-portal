from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Resource(models.Model):
    class ResourceType(models.TextChoices):
        DATASET = "dataset", "Dataset"
        PAPER = "paper", "Research paper"

    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    resource_type = models.CharField(
        max_length=10,
        choices=ResourceType.choices,
    )
    file = models.FileField(upload_to="resources/%Y/%m/")
    country = models.CharField(max_length=100, blank=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    projects = models.ManyToManyField(
        Project,
        related_name="resources",
        blank=True,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
