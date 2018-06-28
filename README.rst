Wraps LGPPP_LOFAR_pipeline pipeline so it is runnable from in the https://github.com/EOSC-LOFAR/lofar_workflow_api

# Install

Should be installed as dependency of https://github.com/EOSC-LOFAR/lofar_workflow_api

To install as standalone
```
pip install https://github.com/EOSC-LOFAR/LGPPP_LOFAR_pipeline.git#egg=LGPPP_LOFAR_pipeline
```

# Run

The wrapper expect the LGPPP_ROOT env var to be set to the directory where pipeline code is installed.

# Development

```
git clone https://github.com/EOSC-LOFAR/LGPPP_LOFAR_pipeline.git .
python setup.py develop
```

## Test


```
export LGPPP_ROOT=$PWD/test
python test.py
```

Should write input and log files to test/ dir.
