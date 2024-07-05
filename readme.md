# snappi extension for IxLoad

This extension allows executing tests written using [snappi](https://github.com/open-traffic-generator/snappi) against  
Cyperf, (one of) Keysight's implementation of [Open Traffic Generator](https://github.com/open-traffic-generator/models/releases).

> The repository is under active development.

## Install on a client

```sh
python -m pip install --upgrade "snappi[cyperf]"
```

## Start scripting

```python
# TODO: add complete description and snippet

import snappi
# host is Cyperf API Server
api = snappi.api(location='https://localhost:8444', ext='cyperf')
# new config
config = api.config()
```

