# Take-home assessment: Profiles

## To run the backend:
From the `src` directory:

`python -m backend.backend`

By default, the server will use port `8080`, use `-p` or `--port` if necessary. Note that you will also need to edit `src/afcu-assessment/proxy.conf.json` to point to the correct port.

## To run the frontend:
From the `src/afcu-assessment` directory:

`ng serve --open --proxy-config proxy.conf.json`

