from kafka import KafkaProducer
import json
import time

# create producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

# load files
with open("data/match_event.json") as f:
    match_events = json.load(f)

with open("data/player_movement.json") as f:
    movements = json.load(f)

with open("data/cheat_alerts.json") as f:
    cheat_alerts = json.load(f)

with open("data/twitch_match.json") as f:
    twitch_messages = json.load(f)


# send match events
for event in match_events:
    producer.send("match_events", value=event)
    print("sent match event")
    time.sleep(0.5)


# send movements
for move in movements:
    producer.send("player_movement", value=move)
    print("sent movement")
    time.sleep(0.5)


# send cheat alerts
for alert in cheat_alerts:
    producer.send("cheat_alerts", value=alert)
    print("sent cheat alert")
    time.sleep(0.5)


# send twitch messages
for msg in twitch_messages:
    producer.send("twitch_chat", value=msg)
    print("sent twitch message")
    time.sleep(0.5)


producer.flush()