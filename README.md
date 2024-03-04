![RabbitMQ](img.png)

# RabbitMQ with Python

Publish and consume messages from RabbitMQ with Python

## Introduction

A **Message Broker** is an intermediary software component that facilites communication and data exchange between
different applications or systems. It plaus a crucial role in supporting a distributed architecture by enabling seamless
communication between various components, even if they running on different plaforms, using differente programming
languages, or have another technologies.

**RabbitMQ** is a Message Broker written in Erlang, that support AMQP protocols and others, designed for works a
distributed, fault-tolerant, soft real-time system with almost 99.999% uptime.

To know more about RabbitMQ, access: [RabbitMQ Documentation](https://www.rabbitmq.com/docs/documentation)

## Setup environment

### Prerequisite

Install the following tools:

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Poetry](https://python-poetry.org/). After installation, configure a Virtual Environment (venv) for this project.

### Quick Start

Open the Command Line Interface (CLI). For example, the Terminal on Ubuntu.

1. Navigate to this project root folder.
2. Execute the folloing command:

```shell
poetry install
```

3. If RabbitMQ cluster is not running, consider to execute the following commands. Otherwise, go to the next step.

```shell
# Open docker folder
cd docker

# Initialize the RabbitMQ cluster.
docker-compose up -d
```

4. After docker is initialized, navigate to this project root folder.

```shell
cd ..
```

5. For each consumer below, open a new CLI window on project root folder, and launch each them like:

```shell
python src/application/direct/consumer_appchat.py
python src/application/direct/consumer_sms.py
```

6. In another CLI window on project root folder, launch the publisher too:

```shell
python src/application/direct/publisher.py
```

Attention: Type CTRL+C, on respectively window, if you want to stop the consumer.

7. When finished, stop the RabbitMQ cluster. Execute the following command on project root folder:

```shell
docker-compose stop
```

Attention: If you want to remove RabbitMQ cluster, execute the following command on project root folder:
```shell
docker-compose down
```
