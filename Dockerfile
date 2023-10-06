FROM python:3.8-slim-bullseye

RUN python -m pip install -U --force-reinstall pip
RUN apt-get update -y && apt-get install -y git libgeos-dev libglib2.0-0


COPY get_region_coord.py /app/get_region_coord.py
RUN git clone https://github.com/cytomine/Cytomine-python-client.git && \
    cd Cytomine-python-client && \
    git checkout v2.2.0 && \
    python setup.py build && \
    python setup.py install

ENTRYPOINT ["python", "/app/get_region_coord.py"]
