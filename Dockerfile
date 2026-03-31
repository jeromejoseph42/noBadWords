FROM python:3.14.3-slim 

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install jupyterlab

COPY . .

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

# To build and run the Docker container, use the following commands:
# docker build -t my-jupyter .
# docker run -it --rm -p 8888:8888 -v "${PWD}:/app" myimage
# http://localhost:8888/lab?token=