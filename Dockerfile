FROM python:3.10

COPY ${PWD} /pcc-rent
WORKDIR /pcc-rent/
RUN pip install -r req.txt
RUN chmod 744 /startup.sh
CMD ["./startup.sh"]
