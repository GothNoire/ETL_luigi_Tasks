import requests
import luigi

class DownloadTaxiTripPark(luigi.Task):
    year = luigi.Parameter()
    month = luigi.Parameter()

    @property
    def filename(self):
        return 'yellow_tripdata_'+self.year+'-'+self.month+'.csv'

    def download_data (self, filename: str) -> requests.Response:
        url = f'https://s3.amazonaws.com/nyc-tlc/trip+data/{filename}'
        response = requests.get(url, stream=True)
        return response

    def run(self):
        response = self.download_data(self.filename)
        with self.output().open('w') as f:
            for rec in response.iter_lines():
                f.write('{}\n'.format(rec.decode('utf-8')))

    def output(self):
        return luigi.LocalTarget('taxi_file/'+self.filename)