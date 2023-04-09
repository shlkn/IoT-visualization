import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "IoT"
org = "test"
token = "RjPXCVFvsn8JhDHxxvMXMw50DHgZ6EF1VpshKbcies44B1R3aEkoI7DSMYaA9pROTTta0aeia1zKH67HaGgLvg=="
# Store the URL of your InfluxDB instance
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 17.5).time("2009-11-10T23:00:00.123456Z")
write_api.write(bucket=bucket, org=org, record=p)