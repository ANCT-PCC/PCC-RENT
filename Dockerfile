FROM python:3.10

COPY ${PWD} /pcc-rent
WORKDIR /pcc-rent/
RUN pip install -r req.txt
RUN sed -e "s/'http://localhost:8080/'/'http://192.168.200.100:8080/'/g" login.js
RUN sed -e "s/'http://localhost:8080/'/'http://192.168.200.100:8080/'/g" admin-db.js
RUN sed -e "s/'http://localhost:8080/'/'http://192.168.200.100:8080/'/g" admin-user.js
RUN sed -e "s/'http://localhost:8080/'/'http://192.168.200.100:8080/'/g" admin-item.js
RUN sed -e "s/'http://localhost:8080/'/'http://192.168.200.100:8080/'/g" admin-top.js
RUN sed -e "s/'http://localhost:8080/'/'http://192.168.200.100:8080/'/g" admintools.js
RUN sed -e "s/'http://localhost:8080/'/'http://192.168.200.100:8080/'/g" dashboard.js
RUN sed -e "s/'http://localhost:8080/'/'http://192.168.200.100:8080/'/g" members.js
RUN sed -e "s/'http://localhost:8080/'/'http://192.168.200.100:8080/'/g" my_rental_list.js
RUN sed -e "s/'http://localhost:8080/'/'http://192.168.200.100:8080/'/g" passwd_change.js
RUN sed -e "s/'http://localhost:8080/'/'http://192.168.200.100:8080/'/g" pcc-items.js
RUN sed -e "s/'http://localhost:8080/'/'http://192.168.200.100:8080/'/g" user_settings.js
CMD ["python", "run.py"]
