from django.test import TestCase, Client
from django.contrib.auth.models import User
from board.models import Board, Task, Membership
from board.const import BOARD_VIEW_COLUMN_COUNT


class BoardTest(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name='test-board', description='sfsdfwefsdfadf')
        self.board.save()
        self.task = Task.objects.create(title='test-task', description='fsdfadf', status='TODO', board=self.board)
        self.task.save()
        self.user = User.objects.create_user('pat', password='haslo123')
        self.user.save()
        self.membership = Membership.objects.create(board=self.board, user=self.user)
        self.membership.save()


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

    def test_membership(self):
        assert Membership.objects.count() == 1
        assert Board.objects.get(id=self.board.id).members.get(board__membership__user_id=self.user.id) == self.user
        assert len(Board.objects.filter(members=self.user)) == 1


class ViewTest(BoardTest):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user)

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

    def test_index_view(self):
        another_board = Board.objects.create(name='another-board', description='bafafw')
        another_board.save()
        assert len(Board.objects.all()) > 1
        response = self.client.get('/')
        response_boards = response.context[0]['board_col']
        assert len(response_boards) <= BOARD_VIEW_COLUMN_COUNT, f'{len(response_boards)}'
        assert len(max(response_boards, key=len)) == response.context[0]['row_count'], \
            f"{len(max(response_boards, key=len))} != {response.context[0]['row_count']}"
