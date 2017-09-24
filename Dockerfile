FROM ubuntu
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install discord pyyaml
RUN mkdir /workspace
ADD *.py /workspace/
ADD *.yml /workspace/
WORKDIR /workspace
ENTRYPOINT python3 /workspace/latticebot.py
