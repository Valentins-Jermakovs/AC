# NGINX GATEWAY

## DESCRIPTION
This Nginx gateway acts as a reverse proxy for all microservices in the system.
It routes incoming requests to the correct FastAPI services (users, projects, news, expenses, events, visits metrics).

It runs inside a shared Docker network to allow communication between containers.

## REQUIREMENTS

Docker installed
All microservices running in the same Docker network (analytics-network)
nginx.conf file configured with service routing rules

## RUNNING THE GATEWAY

Run the Nginx container using the following command:

```
    docker run -d
    --name gateway-nginx
    --network analytics-network
    -p 8080:80
    -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro
    nginx:latest
```

## EXPLANATION

- --name gateway-nginx → container name
- --network analytics-network → shared Docker network for microservices communication
- -p 8080:80 → exposes gateway on localhost:8080
- -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro → mounts custom Nginx config as read-only
- nginx:latest → official Nginx image

## NOTES

- Ensure all microservices are reachable inside analytics-network
- nginx.conf must define upstream services and routing rules
- Gateway acts as single entry point for all API requests