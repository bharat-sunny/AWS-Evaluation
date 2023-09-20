# tests/unit/orders.py

import unittest
import json
from unittest.mock import patch, MagicMock
from lambdas.orders.orders import add_order, fetch_order, delete_order, update_order
from lambdas.users.users import add_user, update_user, delete_user, fetch_user

class TestOrdersFunctions(unittest.TestCase):

    def test_fetch_order_not_found(self):

        # Sample event
        event = {
            'body': '{"order_id": "123"}'
        }

        # Call the function
        response = fetch_order(event)

        # Asserts
        self.assertEqual(response['statusCode'], 404)

    def test_update_order(self):

        # Sample event
        event = {
            'body': '{"order_id": "123", "email": "updated@example.com", "orders": "updated_order"}'
        }

        # Call the function
        response = update_order(event)

        # Asserts
        self.assertEqual(response['statusCode'], 200)

    def test_delete_order(self):

        # Sample event
        event = {
            'body': '{"order_id": "123"}'
        }

        # Call the function
        response = delete_order(event)

        # Asserts
        self.assertEqual(response['statusCode'], 200)

    def test_add_user(self):
        # Sample event
        event = {
            'body': json.dumps({'user_id': '123', 'email': 'test@example.com'}),
            'httpMethod': 'POST'
        }

        response = add_user(event)

        # Asserts
        self.assertEqual(response['statusCode'], 200)

    def test_update_user(self):
        # Sample event
        event = {
            'body': json.dumps({'user_id': '123', 'email': 'updated@example.com'}),
            'httpMethod': 'PUT'
        }

        response = update_user(event)

        # Asserts
        self.assertEqual(response['statusCode'], 200)

    def test_delete_user(self):
        # Sample event
        event = {
            'body': json.dumps({'user_id': '123'}),
            'httpMethod': 'DELETE'
        }

        response = delete_user(event)

        # Asserts
        self.assertEqual(response['statusCode'], 200)


    def test_fetch_user_not_found(self):
        # Sample event
        event = {
            'body': json.dumps({'user_id': '123'}),
            'httpMethod': 'GET'
        }

        response = fetch_user(event)

        # Asserts
        self.assertEqual(response['statusCode'], 404)


if __name__ == '__main__':
    unittest.main()
