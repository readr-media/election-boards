from django.test import TestCase

from .models import Boards
from candidates.models import Candidates, Terms
from django.contrib.gis.geos import Point

from rest_framework import status

# Create your tests here.
class BoardsViewTest(TestCase):
    """test view for boards"""
    def test_boards_url_exists(self):
        """test if /api/boards exists"""
        response = self.client.get('/api/boards')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
    
    def test_boards_url_not_exists(self):
        response = self.client.get('/api/boards/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ChecksViewTest(TestCase):
    """test view for Checks"""    
    def setUp(self):
        test_candidate1 = Candidates.objects.create(
            name='Can'
        ) 
        test_term1 = Terms.objects.create(
            election_year='2018',
            candidate=test_candidate1,
            constituency=1
        )
        test_term2 = Terms.objects.create(
            election_year='2020',
            candidate=test_candidate1,
            constituency=2
        )
        test_board1 = Boards.objects.create(
            image='https://random.cat/view/1321', 
            coordinates=Point(22.6079361,120.2968442), 
            uploaded_by='8094c371-027e-420d-bfae-63df35d1c76d'
        )
        test_board1.candidates.add(test_term1)
        test_board2 = Boards.objects.create(
            image='https://random.cat/view/174', 
            coordinates=Point(22.6079361,120.2968442), 
            uploaded_by='8094c371-027e-420d-bfae-63df35d1c76d'
        )
        test_board2.candidates.add(test_term2)

    def test_checks_list(self):
        """simple test if /api/verify/board return 200"""
        response = self.client.get('/api/verify/board')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_checks_filter_by_election_year(self):
        """test if election_year filter works"""
        response = self.client.get('/api/verify/board?election_year=2018')
        replied_candidates = response.data.get('candidates')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for c in replied_candidates:
            self.assertEqual(c['election_year'], '2018')
