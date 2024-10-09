import unittest
from core.config import QueueConfig, QueueParameters
from core.queue.rabbit_mq import RabbitMQ

class TestRabbitConnection(unittest.TestCase):

    def setUp(self):
    
        self.mock_param = QueueConfig(
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

        self.rabbit = RabbitMQ(self.mock_param)

    def test_connection(self):
        self.rabbit.connect()
        self.assertTrue(self.rabbit.is_connected())

    def test_queue_declaration(self):
        self.rabbit.connect()
        self.rabbit.initialize() 

        original_queue = [queue['name'] for queue in self.mock_param.parameters.queues]
        
        declared_queue = self.rabbit.declared_queues

        self.assertEqual(original_queue, declared_queue)
