# load_test_locus_example

It is a repo for doing a load test by inserting records to local mongodb docker container

### conda env
- python 3.9
```
conda activate load_test
```

- install python packages
```
pip insall --no-cache-dir -r requirements.txt
```

### docker container
```
docker pull mongo
```

```
docker run --name mongodb -d -p 27017:27017 -v /db_data:/data/db mongo
```

### run locust load test
```
locust --users 1200 --spawn-rate 100 -f locustfile.py
```

### Remarks
- https://www.youtube.com/watch?v=L5Tjh19540I
- https://sumanthkumarc.medium.com/testing-mongodb-on-kubernetes-with-locust-first-impressions-part-2-7a5d68213efb