# ./Dockerfile

FROM python:3.10-slim

WORKDIR /src/

COPY src ./

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

RUN chmod +x start.sh

ENTRYPOINT ["./start.sh"]
