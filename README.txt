A stock market predict from Brazilian companies using Recurrent Neural Networks

The idea:
    Using a Recurrent Neural Network to predict if the stock price will fall or ride up,
    base on the price of the previous days.

How to use:
    you need docker installed on your machine.
    go to training folder and run docker-compose up -d.
    after that enter on the container using docker exec -ti <container-id> /bin/bash
    go to data/scrapers and run scrapy crawl <name-of-your-spider>
    the data will be collected to your mongodb.
    then go to ../../models/ and run python <file-of-your-model>.py
    if you want to see the logs with TensorBoard, go to training folder
    and run tensorboard --logdir=logs, after that go to localhost:8080 on your browser.
    if you want to serve your models, stop your container of training using docker stop <container-id>
    go to service, run docker-compose up -d and go to localhost:8080.