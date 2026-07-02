from rest_framework.test import APITestCase


class TodoApiTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'tester',
            'email': 'tester@example.com',
            'password': 'password123',
            'age': 25,
        }
        self.client.post('/api/user/create/', self.user_data, format='json')

    def get_auth_headers(self):
        response = self.client.post(
            '/api/login/',
            {'email': self.user_data['email'], 'password': self.user_data['password']},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_update_and_delete_task_for_authenticated_user(self):
        self.get_auth_headers()

        create_response = self.client.post(
            '/api/tasks/',
            {'title': 'Write API docs', 'description': 'Document the new endpoints', 'completed': False},
            format='json',
        )
        self.assertEqual(create_response.status_code, 201)
        task_id = create_response.data['id']

        update_response = self.client.patch(
            f'/api/tasks/{task_id}/',
            {'title': 'Write final API docs', 'completed': True},
            format='json',
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data['title'], 'Write final API docs')
        self.assertTrue(update_response.data['completed'])

        delete_response = self.client.delete(f'/api/tasks/{task_id}/')
        self.assertEqual(delete_response.status_code, 204)

        list_response = self.client.get('/api/tasks/')
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.data, [])
