# ETL_luigi_Tasks

RUN:

start "luigid" for monitoring your tasks (127.0.0.1:8082)

and

python -m luigi --module DownloadTaxiModule YellowTaxiDateRangeTask --start 2021-01 --stop 2021-03 --workers 3

Also you can start ETL task in local mode

python -m luigi --module DownloadTaxiModule YellowTaxiDateRangeTask --start 2019-01 --stop 2019-02 --local-scheduler

Docker:

docker build -t taxi .

start "luigid" for monitoring your tasks (127.0.0.1:8082 or http://localhost:8082/)

docker run -d --network host taxi luigid

run tasks in interactive mode (start&stop input parameters):

docker run -i --network host taxi python -m luigi --module DownloadTaxiModule YellowTaxiDateRangeTask --start 2019-01 --stop 2019-03 --workers 3
