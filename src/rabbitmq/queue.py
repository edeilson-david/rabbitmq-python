
class Queue(object):
    """
    A queue is a buffer that stores messages sent by producers until consumers are ready to process them.
    It acts as a holding place for messages, enabling asynchronous communication between different components or systems.
    Messages are sent to a specific queue and then consumed by applications or services.

    Key characteristics of RabbitMQ queues include:
    Message Storage: Queues store messages until they are consumed by consumers.
        This allows for decoupling between producers and consumers, as producers can send messages without worrying about
        whether consumers are ready to process them immediately.

    FIFO (First-In-First-Out) Order: Messages in a queue are typically processed in the order they are received, following the FIFO principle.

    Durability: Queues can be durable, meaning they survive broker restarts.
        This ensures that the messages and the queue itself are not lost even if the RabbitMQ server goes down and then restarts.

    Exclusive Queues: Queues can be exclusive, meaning they are used by only one connection and deleted once that connection closes.
        This is useful in scenarios where a queue is meant for a specific consumer.

    Auto-Delete Queues: Queues can be set to automatically delete themselves when no consumers are connected to them.

    Producers publish messages to exchanges, and exchanges route messages to queues based on routing rules.
        Consumers then subscribe to specific queues and retrieve messages for processing.


    """

    def __init__(self, name: str) -> None:
        self.name: str = name
