from django.test import TestCase
from django.urls import reverse
from .models import Candidate, Vote


class VotingFlowTests(TestCase):
    def setUp(self):
        self.candidate = Candidate.objects.create(
            name="Demo Candidate",
            party="Demo Party",
            image="images/c1.webp",
            active=True,
        )

    def test_home_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_health(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok", "service": "votesecure"})

    def test_vote_hash_is_stored_not_plain_identifier(self):
        response = self.client.post(
            reverse("vote"),
            {
                "voter_id": "DEMO123",
                "aadhaar_id": "",
                "candidate": self.candidate.pk,
            },
        )
        self.assertRedirects(response, reverse("success"))
        self.assertEqual(Vote.objects.count(), 1)
        vote = Vote.objects.first()
        self.assertNotEqual(vote.verification_hash, "DEMO123")
        self.assertEqual(len(vote.verification_hash), 64)

    def test_duplicate_vote_is_rejected(self):
        payload = {
            "voter_id": "DEMO999",
            "aadhaar_id": "",
            "candidate": self.candidate.pk,
        }
        self.client.post(reverse("vote"), payload)
        response = self.client.post(reverse("vote"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vote.objects.count(), 1)
