# Take-home assessment: Profiles

## To run the backend:
From the `src` directory:

`python -m backend.backend`

By default, the server will use port `8080`, use `-p` or `--port` if necessary. Note that you will also need to edit `src/afcu-assessment/proxy.conf.json` to point to the correct port.

The server hosts a HTML/CSS/Javascript implementation at `/profile`.

## To run the Angular frontend:
From the `src/afcu-assessment` directory:

`ng serve --open --proxy-config proxy.conf.json`

