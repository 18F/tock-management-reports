# tock-management-reports

A couple of scripts I use to monitor Tock data.

## Usage

For a given `<date>`, just run:
```sh
python run.py <date>
# python run.py 2016-10-23
```

Check an individual, just run:
```sh
python check_user.py <date> <username>
# python check_user.py 2016-10-23 <vladlen.zvenyach>
```

## Installation

You'll need to use some sort of strategy to export the environment variables in `.env.` I use [autoenv](https://github.com/kennethreitz/autoenv). Then:

``` sh
git clone git@github.com:18F/tock-manangement-reports.git
cd tock-management-reports
cp .env.example .env
pyvenv env
source env/bin/activate
pip install requirements.txt
```

# License

CC0-1.0
