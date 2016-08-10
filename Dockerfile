FROM andrewosh/binder-base

MAINTAINER Fabien Benureau <fabien.benureau@gmail.com>

USER main

ADD requirements.txt requirements.txt
RUN python --version
RUN /home/main/anaconda2/envs/python3/bin/pip install -r requirements.txt
RUN jupyter nbextension enable --py --sys-prefix widgetsnbextension
