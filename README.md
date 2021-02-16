# Postgresql DB
## Run on docker
```
$ docker-compose --env-file <path-to-envfile> up -d <service-name>
(Example)
$ docker-compose --env-file ./.env.d/pg.env.development up -d postgres
```

## Stop container
```
$ docker stop <container name>
(Example)
$ docker stop postgres_server
```

## Login postgres from host
Install postgresql client.
```
$ sudo apt install postgresql-client
```
Login.
```
$ psql -U <user> -h <host> -p <port> -d <db-name>
(Example)
$ psql -U user_dev -h 127.0.0.1 -p 5432 -d postgres_dev
```
