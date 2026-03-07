# Real-Time Esports Analytics Pipeline

## Project Goal

Modern esports teams require rapid insights during matches to gain a competitive advantage. This project aims to build a **real-time analytics pipeline** capable of ingesting, processing, and analyzing gameplay events as they occur.

The system is designed to support several analytical capabilities:

- Predict potential **enemy strategies during live tournaments**
- Analyze **player performance metrics**
- Detect **suspicious or cheating patterns**
- Generate **instant post-match analytical reports**

At the current stage, the system uses **sample JSON datasets** to simulate real-time gameplay events. These datasets mimic streams of match events and player activity that would normally be produced by a live game telemetry system.

---

## System Architecture

The pipeline is designed as a **stream-first architecture** for handling continuous event data.

### Data Flow

```
Event Simulation (JSON Events)
        ↓
Kafka (Event Streaming Layer)
        ↓
Apache Flink (Stream Processing)
        ↓
Data Storage Layer
   • PostgreSQL (Hypertables for historical analytics)
   • Redis (Fast lookups & caching)
        ↓
Grafana Dashboard (Real-time monitoring)
        ↓
Machine Learning Models (Prediction layer integrated into Flink)
```

### Components

**Apache Kafka**  
Acts as the central event streaming platform responsible for ingesting and distributing gameplay events across the pipeline.

**Apache Flink (PyFlink)**  
Processes incoming event streams in real time, performing transformations, aggregations, and pattern detection.

**PostgreSQL (Hypertables)**  
Stores structured historical data for deeper analytics and reporting.

**Redis**  
Used as a fast in-memory datastore for quick lookups and low-latency queries.

**Grafana**  
Provides real-time visualization and dashboards for monitoring gameplay metrics and analytical outputs.

**Machine Learning Integration**  
Prediction models will be integrated into the Flink processing layer to enable live inference on streaming data.

---

## Current Progress

The foundational infrastructure of the pipeline has been implemented.

Completed work includes:

- Development of an **event ingestion pipeline**
- Simulation of real-time events using **JSON datasets**
- Initial configuration of core services
- **Containerized deployment using Docker**
- Setup of the streaming stack components

This stage focuses on establishing a **reliable streaming architecture** before implementing advanced analytical features.

---

## Design Decisions

Several architectural choices were made to ensure scalability and real-time performance.

### PyFlink for Stream Processing

PyFlink was selected for the stream processing layer due to:

- Native support for **event-driven stream processing**
- Compatibility with **Apache Flink's distributed architecture**
- Availability of the **Table API**, which simplifies complex stream transformations and analytical queries
- Strong suitability for **low-latency analytics workloads**

Using PyFlink also allows the project to remain within the Python ecosystem while leveraging the performance and reliability of Flink.

---

## Future Improvements

The project will be extended with additional capabilities to enhance the analytical power of the pipeline.

Planned enhancements include:

- Integration of **machine learning models** for predictive analytics
- Implementation of **cheat detection logic**
- Development of **advanced real-time dashboards**
- Integration of **OpenCV** to process visual gameplay data and extract additional insights from video streams
- Expansion of event schemas to support richer gameplay telemetry

These improvements will transform the pipeline from a foundational streaming system into a **comprehensive real-time esports intelligence platform**.
