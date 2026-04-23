import kafka
import json
import time

# create producer
producer = kafka.KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

# load files
with open("data/match_event.json") as f:
    match_events = json.load(f)

with open("data/matches.json") as f:
    matches = json.load(f)

# send match events
for event in match_events:
    producer.send("match_events", value=event)
    print("sent match event")
    time.sleep(0.5)

# send matches
for match in matches:
    producer.send("matches", value=match)
    print("sent match")
    time.sleep(0.5) 


producer.flush()