import unittest
from app import app, get_mongo_client
from pymongo.collection import Collection

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


class APITestCase1(unittest.TestCase):
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

        # Extract the entry ID from the database using the database client
        client = get_mongo_client().Gradebook
        collection = client[self.subject]
        entry = collection.find_one({'student_name': 'John Doe', 'assignment_name': 'Essay'})
        self.test_entry_id = str(entry['_id'])

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
        self.test_add_entry()

        response = self.app.post(f'/{self.subject}/delete/{self.test_entry_id}',
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Existing Entry Data', response.data)


class APITestCase2(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.subject = "Literacy"
        self.test_entry_id = None

    def test_add_entry(self):
        response = self.app.post(f'/{self.subject}/add', data=dict(
            student='Samantha Smith',
            assignment='Spelling Test',
            grade='B',
            teacher='Mr. Robert'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Samantha Smith', response.data)

        # Extract the entry ID from the database using the database client
        client = get_mongo_client().Gradebook
        collection = client[self.subject]
        entry = collection.find_one({'student_name': 'Samantha Smith', 'assignment_name': 'Spelling Test'})
        self.test_entry_id = str(entry['_id'])

    def test_edit_entry(self):
        # Run the test_add_entry method to create a test entry
        self.test_add_entry()

        response = self.app.post(f'/{self.subject}/edit/{self.test_entry_id}',
                                 data=dict(
                                     student='Samantha Willimas',
                                     assignment='Grammar Test',
                                     grade='A',
                                     teacher='Mr. Robert'
                                 ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Samantha Willimas', response.data)
        self.assertIn(b'Grammar Test', response.data)
        self.assertIn(b'A', response.data)
        self.assertIn(b'Mr. Robert', response.data)

    def test_delete_entry(self):
        self.test_add_entry()

        response = self.app.post(f'/{self.subject}/delete/{self.test_entry_id}',
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Existing Entry Data', response.data)

if __name__ == '__main__':
    unittest.main()

