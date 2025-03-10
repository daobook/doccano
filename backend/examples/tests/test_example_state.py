from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.api.utils import (CRUDMixin, make_doc, make_example_state, make_user, prepare_project)


class TestExampleStateList(CRUDMixin):

    @classmethod
    def setUpTestData(cls):
        cls.non_member = make_user()
        cls.project = prepare_project()
        cls.example = make_doc(cls.project.item)
        for user in cls.project.users:
            make_example_state(cls.example, user)
        cls.url = reverse(viewname='example_state_list', args=[cls.project.item.id, cls.example.id])

    def test_returns_example_state_to_project_member(self):
        for member in self.project.users:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data['count'], 1)

    def test_does_not_return_example_state_to_non_project_member(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_does_not_return_example_state_to_unauthenticated_user(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)


class TestExampleStateConfirm(CRUDMixin):

    def setUp(self):
        self.project = prepare_project()
        self.example = make_doc(self.project.item)
        self.url = reverse(viewname='example_state_list', args=[self.project.item.id, self.example.id])

    def test_allows_member_to_confirm_example(self):
        for member in self.project.users:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data['count'], 0)
            self.assert_create(member, status.HTTP_201_CREATED)  # confirm
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data['count'], 1)
            self.assert_create(member, status.HTTP_201_CREATED)  # toggle confirm
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data['count'], 0)


class TestExampleStateConfirmCollaborative(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(collaborative_annotation=True)
        self.example = make_doc(self.project.item)
        self.url = reverse(viewname='example_state_list', args=[self.project.item.id, self.example.id])

    def test_initial_state(self):
        for user in self.project.users:
            response = self.assert_fetch(user, status.HTTP_200_OK)
            self.assertEqual(response.data['count'], 0)

    def test_can_approve_state(self):
        admin = self.project.users[0]
        self.assert_create(admin, status.HTTP_201_CREATED)
        for user in self.project.users:
            response = self.assert_fetch(user, status.HTTP_200_OK)
            self.assertEqual(response.data['count'], 1)
