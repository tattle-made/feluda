import unittest
import pika
import os
from core.config import QueueConfig, QueueParameters
from core.queue.rabbit_mq import RabbitMQ

class TestRabbitConnection(unittest.TestCase):

    def setUp(self):
    
        mock_param = QueueConfig(
            label='RabbitMQ',
            type='RabbitMQ',
            parameters=QueueParameters(
                host_name='localhost',
                queues=[
                    {'name': 'tattle-search-index-queue'},
                    {'name': 'tattle-search-report-queue'}
                ]
            )
        )

        self.rabbit = RabbitMQ(mock_param)

    def test_connection(self):
        self.rabbit.connect()
        self.assertTrue(self.rabbit.is_connected())

    def test_queue_declaration(self):
        self.rabbit.connect()
        self.rabbit.initialize() 

if __name__ == "__main__":
    unittest.main()
