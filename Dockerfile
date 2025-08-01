FROM stb__core:v0.1.0

WORKDIR /stb

ADD src ./

CMD [ "python3", "main.py" ]
