# from django.test import TestCase
# from rest_framework.test import APIClient
# from django.contrib.auth.hashers import make_password

# class TokenObtainTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         # Create a test customer with a hashed password
#         self.customer = Customer.objects.create(
#             email='m12shetty@gmail.com',
#             first_name='Manya',  # This will be used as the username
#             last_name='Shetty',
#             password=make_password('manya')  # Ensure the password is hashed
#         )

#     def test_obtain_token(self):
#         # Attempt to obtain token using first name as username
#         response = self.client.post('/api/token/', {
#             'username': 'Manya',  # This should match first_name
#             'email': 'm12shetty@gmail.com',
#             'password': 'manya'
#         })
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('access', response.data)  # Check for access token in response

#     def test_obtain_token_invalid_username(self):
#         # Attempt to obtain token with invalid username
#         response = self.client.post('/api/token/', {
#             'username': 'InvalidName',  # Invalid first name
#             'email': 'm12shetty@gmail.com',
#             'password': 'manya'
#         })
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_obtain_token_invalid_email(self):
#         # Attempt to log in with invalid email
#         response = self.client.post('/api/token/', {
#             'username': 'Manya',
#             'email': 'wrongemail@gmail.com',
#             'password': 'manya'
#         })
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_obtain_token_invalid_password(self):
#         # Attempt to log in with invalid password
#         response = self.client.post('/api/token/', {
#             'username': 'Manya',
#             'email': 'm12shetty@gmail.com',
#             'password': 'wrongpassword'
#         })
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
