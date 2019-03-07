# Senseye dashboard

Senseye dashboard is a browser-based GUI for the [Senseye](https://github.com/RSchleutker/senseye) monitoring system using the Flask framework.

## Getting started

### Prerequisites

* Python 3
* pip
* wheels
* waitress or another python package providing a server.

Additionally you should have setup the Senseye monitoring system as described on the projects site.

### Installing

To get started download the `senseye_dashboard-x.x-py3-none-any.whl` file from the `/dist` folder and install it by running

```
pip install senseye_dashboard-x.x-py3-none-any.whl
```

### Setting up

Setting the dashboard up is easy. Just save the following lines in a file and run it.

```
import waitress
from senseye_dashboard import create_app

database = '<server>'

waitress.serve(create_app(database = database), port = 54321)
```

The dashboard expects all the tables to be already present in the database, which should be the case if you have already install the Senseye core system. Thats it. Go to your browser and have a look to the dashboard.