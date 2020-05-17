from django.test import TestCase, Client
from django.contrib.auth.models import User
from board.models import Board, Task


class BoardTest(TestCase):
    def setUp(self) -> None:
        self.board_name = 'test-board'
        board = Board.objects.create(name=self.board_name, description='sfsdfwefsdfadf')
        board.save()
        task = Task.objects.create(title='test-task', description='fsdfadf', status='TODO', board=board)
        task.save()
        self.user = User.objects.create_user('pat', password='haslo123')
        self.user.save()


class ModelTest(BoardTest):
    def test_board(self):
        assert Board.objects.count() == 1
        assert Board.objects.first().name == 'test-board'
        assert Board.objects.first().description == 'sfsdfwefsdfadf'

    def test_task(self):
        assert Task.objects.count() == 1
        assert Task.objects.first().title == 'test-task'
        assert Task.objects.first().description == 'fsdfadf'
        assert Task.objects.first().status == 'TODO'


class ViewTest(BoardTest):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.client.login(username='pat', password='haslo123')

    def test_updatetaskstate_view(self):
        task = Task.objects.first()
        assert task.status == 'TODO'
        response = self.client.post('/update-task/', {'state': 'DONE', 'id': task.id})
        assert response.json()['success'] == 'true', f'Wrong json response: {response}'
        assert Task.objects.get(id=task.id).status == 'DONE'

    def test_board_view(self):
        board = Board.objects.first()
        response = self.client.get(f'/board/{board.id}/')
        assert response.status_code == 200
        assert response.context[0]['board'].id == board.id
        assert len(response.context[0]['done_tasks']) == 0
        assert len(response.context[0]['doing_tasks']) == 0
        assert len(response.context[0]['todo_tasks']) == 1
