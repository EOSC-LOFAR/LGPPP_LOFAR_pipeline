import json
import os
import tempfile
import uuid
from os import path
import subprocess

def give_name():
    jsonfile = give_config()
    name = list(jsonfile.keys())[0]
    return name

def give_version():
    return "0.0"

def give_config():
    json_config_file = os.path.join(os.path.dirname(__file__), "data", "config.json")
    with open(json_config_file) as json_data:
        return json.load(json_data)

def give_argument_names(required=False):
    jsonfile = give_config()
    name = list(jsonfile.keys())[0]
    required = jsonfile[name]["schema"]["required"]
    properties = set(jsonfile[name]["schema"]["properties"].keys())
    if required:
        return required
    else:
        return properties


def write_observations(observation, fn):
    srm_uris = observation.split('|')
    with open(fn, 'w') as f:
        for srm_uri in srm_uris:
            f.write(srm_uri + '\n')


def write_config(config, fn):
    with open(fn, 'w') as f:
        f.write('''AVG_FREQ_STEP   = {avg_freq_step}
AVG_TIME_STEP   = {avg_time_step}
DO_DEMIX        = {do_remix}
DEMIX_FREQ_STEP = {demix_freq_step}
DEMIX_TIME_STEP = {demix_time_step}
DEMIX_SOURCES   = {demix_sources}
SELECT_NL       = {select_nl}
PARSET		= {parset}
'''.format(**config))


def run(target, obs_fn, config_fn, job_id):
    stdoutfn = path.join(target, 'stdout.' + job_id + '.txt')
    stderrfn = path.join(target, 'stderr.' + job_id + '.txt')
    cmdfn = path.join(target, 'LGPPP_LRT.py')
    with open(stdoutfn, 'w') as stdout, open(stderrfn, 'w') as stderr:
        subprocess.run([cmdfn, obs_fn, config_fn], cwd=target, stdout=stdout, stderr=stderr)


def run_pipeline(observation, **config):
    pdir = os.environ['LGPPP_ROOT']
    job_id = str(uuid.uuid4())

    obs_fn = path.join(pdir, 'srm.' + job_id + '.txt')
    write_observations(observation, obs_fn)
    config_fn = path.join(pdir, 'master_setup.' + job_id + '.cfg')
    write_config(config, config_fn)

    run(pdir, obs_fn, config_fn, job_id)

    return 'Input and log files *.' + job_id + '.* in dir ' + pdir
