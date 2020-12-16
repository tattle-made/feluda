from services.mq import get_mq_instance


class QueueController:
    def __init__(self):
        self.queue = get_mq_instance()

    def connect(self):
        self.queue.connect()

    def declare_queues(self):    
        self.queue.channel.queue_declare(
            queue='tattle-search-index-queue', durable=True)
        self.queue.channel.queue_declare(
            queue='tattle-search-report-queue', durable=True)

    def add_data_to_index_queue(self, payload):
        self.queue.publish_to_queue(
            queue_name='tattle-search-index-queue', payload=payload)

    def add_data_to_report_queue(self, payload):
        self.queue.publish_to_queue(
            queue_name='tattle-search-report-queue', payload=payload)

    def start_consuming(self, queue_name, callback):
        self.queue.channel.basic_consume(queue=queue_name,
                      on_message_callback=callback)

        print(' [*] Waiting for messages. To exit press CTRL+C ')
        self.queue.channel.start_consuming()


queue_controller = QueueController()
