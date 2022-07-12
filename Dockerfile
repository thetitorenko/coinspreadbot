FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY /source/service_account.json /root/.config/gspread/

COPY script.py .

CMD [ "python", "script.py" ]