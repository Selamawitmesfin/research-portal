from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect

from .forms import ResourceForm
from pathlib import PurePosixPath

from django.db.models import Count, Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, render

from .models import Project, Resource


def overview(request):
    context = _resource_context(request, None, "resources")

    context.update({
        "active_projects": Project.objects.filter(is_active=True).count(),
        "total_resources": Resource.objects.count(),
        "dataset_count": Resource.objects.filter(
            resource_type=Resource.ResourceType.DATASET,
        ).count(),
        "paper_count": Resource.objects.filter(
            resource_type=Resource.ResourceType.PAPER,
        ).count(),
    })

    return render(request, "catalogue/overview.html", context)


def _resource_context(request, resource_type, context_name):
    resources = Resource.objects.all()

    if resource_type is not None:
        resources = resources.filter(resource_type=resource_type)

    query = request.GET.get("q", "").strip()
    country = request.GET.get("country", "").strip()
    file_format = request.GET.get("format", "").strip().lower()

    query = request.GET.get("q", "").strip()
    country = request.GET.get("country", "").strip()
    file_format = request.GET.get("format", "").strip().lower()

    countries = list(
        resources.exclude(country="")
        .order_by("country")
        .values_list("country", flat=True)
        .distinct()
    )

    formats = sorted({
        PurePosixPath(name).suffix.lstrip(".").lower()
        for name in resources.values_list("file", flat=True)
        if name and PurePosixPath(name).suffix
    })

    if query:
        resources = resources.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(projects__name__icontains=query)
        )

    if country:
        resources = resources.filter(country=country)

    if file_format:
        resources = resources.annotate(
            normalized_file=Lower("file"),
        ).filter(
            normalized_file__endswith=f".{file_format}",
        )

    resources = (
        resources.distinct()
        .prefetch_related("projects")
        .order_by("-uploaded_at")
    )

    return {
        context_name: resources,
        "query": query,
        "selected_country": country,
        "selected_format": file_format,
        "countries": countries,
        "formats": formats,
    }


def paper_list(request):
    context = _resource_context(
        request,
        Resource.ResourceType.PAPER,
        "papers",
    )

    return render(request, "catalogue/paper_list.html", context)


def dataset_list(request):
    context = _resource_context(
        request,
        Resource.ResourceType.DATASET,
        "datasets",
    )

    return render(request, "catalogue/dataset_list.html", context)


def project_list(request):
    projects = Project.objects.annotate(
        resource_count=Count("resources", distinct=True),
    ).order_by("name")

    return render(
        request,
        "catalogue/project_list.html",
        {"projects": projects},
    )
def project_resources(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    resources = (
        project.resources.all()
        .order_by("-uploaded_at")
    )

    return render(
        request,
        "catalogue/project_resources.html",
        {
            "project": project,
            "resources": resources,
        },
    )
@staff_member_required(login_url="admin:login")
def resource_upload(request):
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES)

        if form.is_valid():
            resource = form.save()

            if resource.resource_type == Resource.ResourceType.PAPER:
                return redirect("catalogue:paper_list")

            return redirect("catalogue:dataset_list")
    else:
        form = ResourceForm()

    return render(
        request,
        "catalogue/resource_upload.html",
        {"form": form},
    )
