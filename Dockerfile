FROM python:3.10

COPY ${PWD} /pcc-rent
WORKDIR /pcc-rent/
RUN pip install -r req.txt
RUN sed -e "s/'http://localhost:8080/'/'http://192.168.200.100:8080/'/g"
CMD ["python", "run.py"]
