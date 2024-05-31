FROM python:3.10

COPY ${PWD} /pcc-rent
WORKDIR /pcc-rent/
RUN pip install -r req.txt
RUN chmod +rx startup.sh
CMD ["chmod", "+rx", "start.sh", "&&", "./start.sh"]
