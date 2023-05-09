# dns-redis
Python DNS server that use redis as backend database

## How dns-redis work?
dns-redis remove dns zone concept. So it use like /etc/hosts in linux that user can add key-value of domain (remove last dot) & ip address.
For prepare database in redis, use redis-cli
```
SET <Domain-without-last-dot> <ip-address>
SET example.com 127.0.0.1
```

## How to run dns-redis
Please setup redis server & add data for dns record
### 1) Run server.py directly
You need to run with environment variable or modify variable in File: server.py
```
pip install -r requirements.txt
REDIS_HOST=172.16.0.1 REDIS_PORT=6379 REDIS_PASSWORD="secret" python server.py
```

### 2) Run with dockker
You need to build docker and run it.
```
docker build -t dns-redis .
docker run -e REDIS_HOST=172.16.0.1 \
  -e REDIS_PORT=6379 \
  -e REDIS_PASSWORD="secret" \
  -p 53:53/udp dns-redis
```

## How to verify dns-redis
You can use dig command to query dns record
```
dig @localhost -p 53 <domain>
dig @localhost -p 53 example.com
```