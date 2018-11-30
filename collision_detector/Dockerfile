FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY python-packages/dencity-bike dencity-bike
RUN pip install --no-cache-dir ./dencity-bike

COPY *.py ./
COPY *.sh ./
ADD projectors ./projectors

CMD ["bash", "./application.sh"]
