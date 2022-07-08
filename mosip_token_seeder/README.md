# MOSIP Token Seeder

Refer [documentation](https://docs.mosip.io/openg2p/mosip-token-seeder).

## Pre-requisites

```sh
virtualenv venv_token_seeder
echo -e '\nexport TOKENSEEDER_GUNICORN__WORKERS=3\nexport TOKENSEEDER_GUNICORN__MAX_REQUESTS=10000\nexport TOKENSEEDER_GUNICORN__TIMEOUT=5\nexport TOKENSEEDER_GUNICORN__KEEP_ALIVE=5' >> venv_token_seeder/bin/activate
echo 'alias run_token_seeder_dev='\''TOKENSEEDER_DB__PASSWORD=$(rm *.dbsqlite; python3 -m mosip_token_seeder.repository db_init) gunicorn -n "gunicorn" --worker-class uvicorn.workers.UvicornWorker --workers ${TOKENSEEDER_GUNICORN__WORKERS} --bind 0.0.0.0:8080 --max-requests ${TOKENSEEDER_GUNICORN__MAX_REQUESTS} --timeout ${TOKENSEEDER_GUNICORN__TIMEOUT} --keep-alive ${TOKENSEEDER_GUNICORN__KEEP_ALIVE} --access-logfile "-" --error-logfile "-" mosip_token_seeder:app'\' >> venv_token_seeder/bin/activate
source venv_token_seeder/bin/activate
pip3 install -r requirements.txt
deactivate
```

## Running
-   ```sh
    source venv_token_seeder/bin/activate
    run_token_seeder_dev
    ```
    Access localhost:8080 on browser. Access localhost:8080/docs for apidocs.
- For running only the authenticator for single authentication:
  - Configure `mosip_auth` section in `config.toml`. And place the certificate and keys appropriately.
  - Then run (sample json given in samples folder):
      ```sh
      python3 -m authenticator demoauth <json>
      ```


## Docker
```sh
docker run -it --rm \
    --name token-seeder \
    -p 8080:8080 \
    <acc>/mosip-openg2p-token-seeder
```