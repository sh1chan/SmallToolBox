FROM stb__core:v0.1.0

WORKDIR /stats_generator

ADD . ./

RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

CMD [ "python3", "src/main.py" ]