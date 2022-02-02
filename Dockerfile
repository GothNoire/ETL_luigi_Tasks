FROM python:3-onbuild

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /code

WORKDIR /code

COPY . /code

#EXPOSE 5000

#CMD ["python", "./DownloadTaxiModule.py"]
