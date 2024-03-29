"""
A Redpanda producer
"""

import os, json
from dataclasses import dataclass

from kafka import KafkaProducer

@dataclass
class ProducerConfig:
    """a Dataclass for storing our producer configs"""

    # the Redpanda bootstrap servers will be pulled from the
    # REDPANDA_BROKERS environment variable. Ensure this is set
    # before running the code
    def __init__(self, topic, bootstrap_servers ) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic

class Producer:
    def __init__(self, config: ProducerConfig):
        # instantiate a Kafka producer client. This client is compatible
        # with Redpanda brokers
        self.client = KafkaProducer(
            bootstrap_servers=config.bootstrap_servers,
            key_serializer=str.encode,
            security_protocol="PLAINTEXT",  
            sasl_mechanism="PLAIN", 
            value_serializer=lambda m: json.dumps(m).encode('ascii'),
        )
        self.topic = config.topic

    def produce(self, message: str, key=None):
        """Produce a single message to a Redpanda topic"""
        try:
            # send a message to the topic
            future = self.client.send(self.topic, key=key, value=message)

            # this line will block until the message is sent (or timeout).
            record_metadata = future.get(timeout=10)

            print(f"Successfully produced message to topic: {self.topic}")

            return record_metadata
        except:
            print(f"Could not produce to topic: {self.topic}")
            raise
