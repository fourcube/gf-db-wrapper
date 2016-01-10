#/usr/bin/env bash
docker run -v /tmp/redis:/data -p 6379:6379 --name some-redis -d redis redis-server --appendonly yes
