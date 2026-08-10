from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import VoteForm
from .models import Candidate, Vote
from .utils import verification_hash


def home(request):
    candidates = Candidate.objects.filter(active=True)
    return render(request, "index.html", {"candidates": candidates})


def about(request):
    return render(request, "c.html")


def vote(request):
    if request.method == "POST":
        form = VoteForm(request.POST)
        if form.is_valid():
            digest = verification_hash(form.cleaned_data["verification_value"])
            candidate = form.cleaned_data["candidate"]

            if Vote.objects.filter(verification_hash=digest).exists():
                form.add_error(None, "This demo verification ID has already voted.")
            else:
                try:
                    Vote.objects.create(
                        verification_hash=digest,
                        candidate=candidate,
                    )
                except IntegrityError:
                    form.add_error(None, "This demo verification ID has already voted.")
                else:
                    return redirect("success")
    else:
        form = VoteForm()

    return render(request, "vote.html", {"form": form})


def success(request):
    return render(request, "s.html")


def results(request):
    candidates = Candidate.objects.filter(active=True).annotate(
        vote_total=Count("votes")
    )
    total_votes = Vote.objects.count()
    return render(
        request,
        "results.html",
        {"candidates": candidates, "total_votes": total_votes},
    )


def health(request):
    return JsonResponse({"status": "ok", "service": "votesecure"})
