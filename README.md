# ETL_luigi_Tasks

RUN:
start "luigid" for monitoring your tasks (127.0.0.1:8082)
and
python -m luigi --module DownloadTaxiModule YellowTaxiDateRangeTask --start 2021-01 --stop 2021-03 --workers 3

Also you can start ETL task in local mode

python -m luigi --module DownloadTaxiModule YellowTaxiDateRangeTask --start 2019-01 --stop 2019-02 --local-scheduler
