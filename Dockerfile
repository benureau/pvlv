FROM andrewosh/binder-base

MAINTAINER Fabien Benureau <fabien.benureau@gmail.com>

USER main

ADD requirements.txt requirements.txt
RUN conda search python
RUN conda create --name snakes python=3
RUN source activate snakes
RUN conda info --envs
RUN python --version
RUN python install -r requirements.txt
RUN jupyter nbextension enable --py --sys-prefix widgetsnbextension
