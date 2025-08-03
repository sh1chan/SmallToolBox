FROM stb__core:v0.2.0

WORKDIR /stb

ADD src ./

CMD [ "python3", "main.py" ]
