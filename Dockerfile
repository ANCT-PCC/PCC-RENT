FROM python:3.10

COPY ${PWD} /pcc-rent
WORKDIR /pcc-rent/
RUN pip install -r req.txt
RUN sed -e "s#'http://localhost:8080/'#'http://192.168.200.100:8080/'#g" static/login.js
RUN sed -e "s#'http://localhost:8080/'#'http://192.168.200.100:8080/'#g" static/admin-db.js
RUN sed -e "s#'http://localhost:8080/'#'http://192.168.200.100:8080/'#g" static/admin-user.js
RUN sed -e "s#'http://localhost:8080/'#'http://192.168.200.100:8080/'#g" static/admin-item.js
RUN sed -e "s#'http://localhost:8080/'#'http://192.168.200.100:8080/'#g" static/admin-top.js
RUN sed -e "s#'http://localhost:8080/'#'http://192.168.200.100:8080/'#g" static/admintools.js
RUN sed -e "s#'http://localhost:8080/'#'http://192.168.200.100:8080/'#g" static/dashboard.js
RUN sed -e "s#'http://localhost:8080/'#'http://192.168.200.100:8080/'#g" static/members.js
RUN sed -e "s#'http://localhost:8080/'#'http://192.168.200.100:8080/'#g" static/my_rental_list.js
RUN sed -e "s#'http://localhost:8080/'#'http://192.168.200.100:8080/'#g" static/passwd_change.js
RUN sed -e "s#'http://localhost:8080/'#'http://192.168.200.100:8080/'#g" static/pcc-items.js
RUN sed -e "s#'http://localhost:8080/'#'http://192.168.200.100:8080/'#g" static/user_settings.js
CMD ["python", "run.py"]
