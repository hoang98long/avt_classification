FROM continuumio/anaconda3

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1-mesa-glx

COPY . /app/avt_classification

RUN conda create --name avt_classification python=3.8  # Thay python=3.8 bằng phiên bản Python mà bạn cần
RUN echo "conda activate avt_classification" >> ~/.bashrc
RUN conda init bash

COPY requirements.txt .
RUN conda run -n avt_classification pip install -r requirements.txt

CMD ["bash", "-c", "source activate avt_classification && cd /app/avt_classification && python main.py --config_file /app/config.json"]