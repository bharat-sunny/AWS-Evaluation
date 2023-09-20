# tests/unit/orders.py

import unittest
from unittest.mock import patch, MagicMock
from lambdas.orders.orders import add_order, fetch_order, delete_order, update_order
import moto

class TestOrdersFunctions(unittest.TestCase):

    # @patch('lambdas.orders.orders.boto3.client')
    # def test_add_order_successful(self, mock_boto_client):
        
    #     # Mock the Lambda invoke call
    #     mock_lambda = MagicMock()
    #     mock_lambda.invoke.return_value = {
    #         'StatusCode': 200,
    #         'Payload': '{"message": "Notification sent"}'
    #     }
    #     mock_boto_client.return_value = mock_lambda
        
    #     # Sample event
    #     event = {
    #         'body': '{"email": "test@example.com", "orders": "sample_order"}'
    #     }

    #     # Call the function
    #     response = add_order(event)

    #     # Asserts
    #     self.assertEqual(response['statusCode'], 200)
    #     mock_lambda.invoke.assert_called_once()

    # def test_fetch_order_found(self):

    #     # Sample event
    #     event = {
    #         'body': '{"order_id": "123"}'
    #     }

    #     # Call the function
    #     response = fetch_order(event)

    #     # Asserts
    #     self.assertEqual(response['statusCode'], 200)

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


if __name__ == '__main__':
    unittest.main()
