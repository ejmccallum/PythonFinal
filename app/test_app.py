import unittest
from app import app


class UITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Colorado Mesa Highschool Gradebook', response.data)

    def test_subject_grades(self):
        subjects = ["History", "Mathematics", "Literacy", "Science"]
        for subject in subjects:
            response = self.app.get(f'/{subject}/grades')
            self.assertEqual(response.status_code, 200)
            self.assertIn(subject.encode(), response.data)

    def test_subject_detail(self):
        subjects = ["History", "Mathematics", "Literacy", "Science"]
        for subject in subjects:
            response = self.app.get(f'/{subject}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(subject.encode(), response.data)


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.subject = "History"
        self.test_entry_id = None

    def test_add_entry(self):
        response = self.app.post(f'/{self.subject}/add', data=dict(
            student='John Doe',
            assignment='Essay',
            grade='A',
            teacher='Mr. Smith'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

        # Extract the entry ID from the response or query it from the database
        entry_id_start = response.data.find(b'Entry ID: ') + len(b'Entry ID: ')
        entry_id_end = response.data.find(b'</p>', entry_id_start)
        self.test_entry_id = response.data[
            entry_id_start:entry_id_end].decode()

    def test_edit_entry(self):
        # Run the test_add_entry method to create a test entry
        self.test_add_entry()

        response = self.app.post(f'/{self.subject}/edit/{self.test_entry_id}',
                                 data=dict(
                                    student='Updated Student',
                                    assignment='Updated Assignment',
                                    grade='B',
                                    teacher='Updated Teacher'
                                     ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Student', response.data)
        self.assertIn(b'Updated Assignment', response.data)
        self.assertIn(b'B', response.data)
        self.assertIn(b'Updated Teacher', response.data)

    def test_delete_entry(self):
        # Run the test_add_entry method to create a test entry
        self.test_add_entry()

        response = self.app.post(f'/{self.subject}/delete/{self.test_entry_id}'
                                 , follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Your Existing Entry Data', response.data)


if __name__ == '__main__':
    unittest.main()
