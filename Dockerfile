FROM python:3.10

COPY ${PWD} /pcc-rent
WORKDIR /pcc-rent/
RUN pip install -r req.txt
CMD ["python","run.py"]
