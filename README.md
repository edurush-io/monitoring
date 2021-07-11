# monitoring plugins

- [check_clickhouse.py](check_clickhouse.py): Basic healtcheck for ClickHouse (https://clickhouse.tech/) (_requires Python 3_)

# Example usage
### check_clickhouse.py - 
```
usage: check_clickhouse.py

Basic check for ClickHouse health (uses HTTP interface)

optional arguments:
  -h, --help           show this help message and exit
  --host HOST          ClickHouse host
  --port PORT          ClickHouse port
  --user USER          ClickHouse user
  --password PASSWORD  ClickHouse password
  --timeout TIMEOUT    Connection timeout
```
