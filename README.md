# Social face recognition
This project aims to bring you the awareness of how many people you meet during your day without realising it.

* People like privacy same as you, so DO NOT expose any of the database/storage publicly.
Remember to respect the LAW!

* Requirements
Python 3
cmake
Docker
Raspeberry PI + PiCam

* Acquisition flow
- Raspeberry acquires all the faces and stores it locally

## Usage
# face_live.py
Runs the acquisition on the fly to test and debug the library


* Docker tips
Elasticsearch
```
docker run -p 9200:9200 -p 9300:9300 \
-e "discovery.type=single-node" \
-e "cluster.routing.allocation.disk.watermark.low=30mb" \
-e "cluster.routing.allocation.disk.watermark.high=20mb" \
-e "cluster.routing.allocation.disk.watermark.flood_stage=10mb" \
-v ${PWD}/esdata:/usr/share/elasticsearch/data \
--name es_face \
-d docker.elastic.co/elasticsearch/elasticsearch:7.16.0
```
Kibana
```
docker run --link es_face:elasticsearch -p 5601:5601 docker.elastic.co/kibana/kibana:7.16.0
```

* ToDo
- Handle ES try/catch on load
- Preload faces
- Add geolocation acquisition
- Evaluate to scarpe public profiles from social networks to match faces
