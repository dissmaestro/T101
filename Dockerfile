FROM python:3.8-slim-buster
RUN ["mkdir","/m_dir"]
COPY lr1.py  /m_dir
WORKDIR /m_dir
CMD ["python3", "lr1.py"]
