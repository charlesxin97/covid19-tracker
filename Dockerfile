FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y \
  gcc

RUN git clone https://github.com/charlesxin97/covid19-tracker

RUN conda install -c conda-forge yarn

RUN cd covid19-tracker && yarn install

RUN pip install --upgrade pip

RUN pip install -r ./requirements.txt

EXPOSE 5000

WORKDIR covid19-tracker