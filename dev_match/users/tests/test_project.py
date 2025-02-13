from django.test import TestCase

from ..models import Project, User


class ProjectTestCase(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="password")
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")

        self.project = Project.objects.create(
            owner=self.owner,
            project_name="Test Project",
            description="A test project",
            maximum_collaborators=2,
            status="RN",
            open_positions=2,
        )

    def test_project_creation(self):
        self.assertEqual(self.project.project_name, "Test Project")
        self.assertEqual(self.project.status, "RN")
        self.assertEqual(self.project.open_positions, 2)

    def test_apply_to_project(self):
        self.project.apllied_collaborators.add(self.user1)
        self.assertIn(self.user1, self.project.get_applied_collaborators())

    def test_accept_contributor(self):
        self.project.apllied_collaborators.add(self.user1)
        self.project.move_from_applied_to_collaborators(self.user1.username)

        self.assertIn(self.user1, self.project.collaborators.all())
        self.assertNotIn(self.user1, self.project.apllied_collaborators.all())
        self.assertEqual(self.project.open_positions, 1)

    def test_decline_contributor(self):
        self.project.apllied_collaborators.add(self.user1)
        self.project.decline_applied_collaborators(self.user1.username)

        self.assertNotIn(self.user1, self.project.apllied_collaborators.all())

    def test_check_collaborator_exists(self):
        self.project.apllied_collaborators.add(self.user1)
        self.assertTrue(self.project.check_collaborator_exists(self.user1.username))
