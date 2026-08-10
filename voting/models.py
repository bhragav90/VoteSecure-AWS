from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    image = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name} — {self.party}"


class Vote(models.Model):
    verification_hash = models.CharField(max_length=64, unique=True, db_index=True)
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.PROTECT,
        related_name="votes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Vote #{self.pk} — {self.candidate.name}"
