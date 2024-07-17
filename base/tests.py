from django.test import TestCase
from django.urls import reverse
from .models import User, Room, Topic, Message

class UserTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com', password='testpassword123')

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(response.wsgi_request.user.is_authenticated)

class RoomTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com', password='testpassword123')
        self.client.login(email='testuser@example.com', password='testpassword123')
        self.topic = Topic.objects.create(name='Test Topic')

    def test_room_creation(self):
        response = self.client.post(reverse('create-room'), {
            'name': 'Test Room',
            'description': 'A test room description',
            'topic': self.topic.id
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Room.objects.filter(name='Test Room').exists())

class MessageTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com', password='testpassword123')
        self.client.login(email='testuser@example.com', password='testpassword123')
        self.topic = Topic.objects.create(name='Test Topic')
        self.room = Room.objects.create(
            host=self.user, topic=self.topic, name='Test Room')

    def test_message_posting(self):
        response = self.client.post(reverse('room', args=[self.room.id]), {
            'body': 'Test message body'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after posting
        self.assertTrue(Message.objects.filter(body='Test message body').exists())
