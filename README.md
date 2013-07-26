A Flask app for searching music review data. 

## Requirements

1. Twitter Bootstrap
    - Unpack into `static/` directory (http://twitter.github.io/bootstrap/index.html)
2. TableSorter 
    - Clone into static (https://github.com/Mottie/tablesorter)
    - This app uses a cutomized bootstrap theme and tablesorter options
3. Add a file in the root directory called config.py containing the following variable definitions

: 

    CSRF_ENABLED = True
    SECRET_KEY = 'key'
    HOST = 'DB hostname'
    DBPASS = 'database password'
    DBNAME = 'database name'
    DBUSER = 'database user name'
