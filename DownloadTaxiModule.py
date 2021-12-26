import csv

import requests
import luigi
from luigi.contrib import sqla
import pandas as pd
from typing import List
from sqlalchemy import Numeric, Date
from luigi.util import requires
from dateutil.relativedelta import relativedelta


def get_filename(year: int, month: int) -> str:
    return f'yellow_tripdata_{year}-{month:02}.csv'

class DownloadTaxiTripPark(luigi.Task):
    date = luigi.MonthParameter()

    @property
    def filename(self): 
        return get_filename(self.date.year, self.date.month)

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

@requires(DownloadTaxiTripPark)
class AggregateTaxiTrip(luigi.Task):
    def group_by_date(self, file, group_by='date', metrics: List[str] = None) -> pd.DataFrame:
        dframe = pd.read_csv(file)
        dframe[group_by] = pd.to_datetime(dframe['tpep_pickup_datetime']).dt.strftime('%Y-%m-%d')
        dframe = dframe.groupby(group_by)[metrics].sum().reset_index()
        return dframe

    @property
    def filename(self):
        return get_filename(self.date.year, self.date.month)

    def run(self):
        with self.input().open() as first_file, self.output().open('w') as aggr_file:
            dframe = self.group_by_date (file=first_file, metrics=['passenger_count', 'trip_distance', 'total_amount'])
            dframe.to_csv(aggr_file.name, index=False)

    def output(self):
        return luigi.LocalTarget('taxi_file/aggr_'+self.filename)

@requires(AggregateTaxiTrip)
class CopyAgrrInfoToSQLliteBBd(sqla.CopyToTable):

    table = 'yellow_NY_trip'
    connection_string = 'sqlite:///sqlite.db'

    columns = [
        (['date', Date()], {}),
        (['passenger_count', Numeric(2)], {}),
        (['trip_distance', Numeric(2)], {}),
        (['total_amount', Numeric(2)], {}),
    ]

    def rows(self):
        with self.input().open() as file:
            df = pd.read_csv(file, parse_dates=[0])
            rows = df.to_dict(orient='split')['data']
            return rows

class YellowTaxiDateRangeTask(luigi.WrapperTask):
    start = luigi.MonthParameter()
    stop = luigi.MonthParameter()

    def requires(self):
        current_month = self.start
        while current_month <= self.stop:
            yield CopyAgrrInfoToSQLliteBBd(date=current_month)
            current_month += relativedelta(months=1)
