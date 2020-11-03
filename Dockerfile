FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y \
  gcc

RUN git clone https://github.com/charlesxin97/covid19-tracker

RUN conda install -c conda-forge yarn

RUN cd covid19-tracker && yarn install

RUN pip install --upgrade pip

COPY requirements.txt /opt/app/requirements.txt

RUN pip install -r /opt/app/requirements.txt

EXPOSE 5000

WORKDIR covid19-tracker