FROM python:3.14.3-slim 

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install jupyterlab

COPY . .

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
# docker build -t my-jupyter .
# docker run -it --rm -p 10000:8888 -v "%cd%":/app my-jupyter
# http://localhost:10000/lab?token=