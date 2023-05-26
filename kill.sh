pkill -9 -f serialsensor.py
D=$(date +%FT%T%z)
curl --location --request POST 'https://telemetry-nyubaja.herokuapp.com/measurement/' \
--header 'Content-Type: application/json' \
--header 'Cookie: Cookie_2=value' \
--data-raw '{
	"sensor_id": 2,
	"values": {
		"log" : "DAQ process sucessfully killed by Pit"
	},
	"date" : "'"$D"'"
}'