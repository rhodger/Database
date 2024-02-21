# Company Database #

This solution is split into two components, a backend and a frontend. Each must be run independently
following the instructions below. The frontend will then be accessible via a web browser at
_http://localhost:3000/_.

## Dependencies ##

Some Python libraries are required to run the backend - these are all available via pip and can be
installed by running:

```bash
python3 -m pip install flask flask_cors thefuzz
```

## Usage ##

The following two sections can be run in any order to start up both the front and back ends.

### Backend ###

The Python backend can be started by running `python3 ./backend.py` from the `<project>/backend`
directory.

### Frontend ###

The Javascript frontend can be started by running `npm start` from the `<project>/frontend`
directory.

## Usage ##

The frontend is accessible via browser at `http://localhost:3000/` and should be straightforward to
use - links shown in blue can be clicked to change the current focus shown in the view below the
search bar.