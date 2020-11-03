FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y \
  gcc

RUN git clone https://github.com/charlesxin97/covid19-tracker

RUN conda install -c conda-forge yarn

RUN cd covid19-tracker && yarn install

RUN pip install --upgrade pip

COPY requirements.txt /opt/app/requirements.txt

COPY resulting.py /opt/app/resulting.py

RUN pip install -r /opt/app/requirements.txt

WORKDIR covid19-tracker

CMD ["bokeh", "serve", "--show", "/opt/app/resulting.py"]