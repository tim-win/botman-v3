FROM arm32v6/alpine:latest

RUN mkdir /botman-v3/

WORKDIR /botman-v3/

ENTRYPOINT ["/botman-v3/entrypoint.sh"]

CMD ["python3 /botman-v3/run.sh"]

RUN apk update && \
    apk add python3

COPY ./requirements.txt /botman-v3/requirements.txt

RUN pip3 install -r /botman-v3/requirements.txt

COPY ./ /botman-v3/