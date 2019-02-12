import unittest
import datetime

from flask_testing import TestCase
from flask import url_for

from app import create_app, db, mail
from app.models import Event, Recipient


class TestBase(TestCase):
    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///test.db'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test event
        event = Event(event_id='31', event_subject='Nowaday', event_content='Test content',
                      timestamp=datetime.datetime(2019, 5, 17))

        recipient = Recipient(name="Grant", email="somerandom_mail@gmail.com", event_id="31")

        # save event to database
        db.session.add(event)
        db.session.add(recipient)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


class TestModels(TestBase):

    def test_event_model(self):
        """
        Test number of record in Event table
        """
        self.assertEqual(Event.query.count(), 1)

    def test_recipient_model(self):
        """
        Test number of record in Event table
        """
        self.assertEqual(Recipient.query.count(), 1)


class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Test homepage view
        """
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)

    def test_create_event_view(self):
        """
        Test create event view
        """
        response = self.client.get(url_for('events.save_event'))
        self.assertEqual(response.status_code, 200)

        # Create a new Event
        response = self.client.post(url_for('events.save_event'), data={
            'event_id': '12',
            'event_subject': 'Bird Box',
            'event_content': 'Blinded by a bird',
            'timestamp': datetime.datetime.now(),
        })
        self.assertEqual(response.status_code, 200)

    def test_save_recipient_view(self):
        """
        Test save recipient view
        """
        response = self.client.get(url_for('recipients.save_recipient'))
        self.assertEqual(response.status_code, 200)

        # Create a new Recipient
        response = self.client.post(url_for('recipients.save_recipient'), data={
            'name': 'Bob',
            'email': 'bob@apolic.com',
            'event_id': '12',
        })
        self.assertEqual(response.status_code, 200)

    def test_show_event_view(self):
        """
        Test show event view
        """
        response = self.client.get(url_for('events.show_events'))
        self.assertEqual(response.status_code, 200)

    def test_show_recipient_view(self):
        """
        Test show recipient view
        """
        response = self.client.get(url_for('recipients.show_recipients'))
        self.assertEqual(response.status_code, 200)

    def test_404(self):
        response = self.client.get('/wrong/url')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data)


if __name__ == '__main__':
    unittest.main()
