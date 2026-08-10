from django.contrib import admin
from .models import Candidate, Vote


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("name", "party", "active", "vote_count")
    list_filter = ("active",)
    search_fields = ("name", "party")

    @admin.display(description="Votes")
    def vote_count(self, obj):
        return obj.votes.count()


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("id", "candidate", "created_at")
    list_filter = ("candidate", "created_at")
    readonly_fields = ("verification_hash", "candidate", "created_at")
    search_fields = ("verification_hash",)
