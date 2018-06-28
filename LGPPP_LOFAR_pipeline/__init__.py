import os
import tempfile
import uuid
from os import path
import subprocess

def give_name():
    return __name__

def give_version():
    return "0.0"

def give_argument_names():
    return {"avg_freq_step", 
            "avg_time_step", 
            "do_demix", 
            "demix_freq_step", 
            "demix_time_step", 
            "demix_sources", 
            "select_NL","parset"}

# def give_schema():
#     schema = \
#         {get_name():{
#             "label": "LOFAR GRID Pre-Processing Pipeline",
#             "schema": {
#                 "type": "object",
#                 "title": "Configuration Parameters:",
#                 "description": "This is the LOFAR GRID Pre-Processing Pipeline. Here we print a description of the pipeline.",
#                 "required": [
#                   "avg_freq_step",
#                   "avg_time_step",
#                   "do_demix",
#                   "demix_freq_step",
#                   "demix_time_step",
#                   "demix_sources",
#                   "select_nl",
#                   "parset"
#                 ],
#                 "properties": {
#                   "avg_freq_step": {
#                     "type": "integer",
#                     "title": "avg_freq_step",
#                     "description": "corresponds to .freqstep in NDPPP .type=average , or in case of .type=demixer it is the demixer.freqstep",
#                     "default": 2,
#                     "minimum": 0,
#                     "exclusiveMinimum": true,
#                     "maximum": 1000,
#                     "exclusiveMaximum": true,    
#                     "propertyOrder": 1
#                   },
#                   "avg_time_step": {
#                     "type": "integer",
#                     "title": "avg_time_step",
#                     "description": "corresponds to .timestep in NDPPP .type=average , or in case of .type=demixer it is the demixer.timestep",
#                     "default": 4,
#                     "minimum": 0,
#                     "exclusiveMinimum": true,
#                     "maximum": 1000,
#                     "exclusiveMaximum": true,    
#                     "propertyOrder": 2
#                   },
#                   "do_demix": {
#                     "type": "boolean",
#                     "title": "do_demix",
#                     "description": "if true then demixer instead of average is performed",
#                     "default": true,
#                     "propertyOrder": 3
#                   },
#                   "demix_freq_step": {
#                     "type": "integer",
#                     "title": "demix_freq_step",
#                     "description": "corresponds to .demixfreqstep in NDPPP .type=demixer",
#                     "default": 2,
#                     "minimum": 0,
#                     "exclusiveMinimum": true,
#                     "maximum": 1000,
#                     "exclusiveMaximum": true,    
#                     "propertyOrder": 4
#                   },
#                   "demix_time_step": {
#                     "type": "integer",
#                     "title": "demix_time_step",
#                     "description": "corresponds to .demixtimestep in NDPPP .type=demixer",
#                     "default": 2,
#                     "minimum": 0,
#                     "exclusiveMinimum": true,
#                     "maximum": 1000,
#                     "exclusiveMaximum": true,    
#                     "propertyOrder": 5
#                   },
#                   "demix_sources": {
#                     "type": "string",
#                     "description": "",
#                     "title": "demix_sources",
#                     "format": "select",
#                     "enum": [
#                       "CasA",
#                       "CygA"
#                     ],
#                     "propertyOrder": 6
#                   },
#                   "select_nl": {
#                     "type": "boolean",
#                     "title": "select_nl",
#                     "description": "if true then only Dutch stations are selected",
#                     "default": true,
#                     "propertyOrder": 7
#                   },
#                   "parset": {
#                     "type": "string",
#                     "title": "parset",
#                     "description": "",
#                     "format": "select",
#                     "enum": [
#                       "",
#                       "hba_npp",
#                       "hba_raw",
#                       "lba_npp",
#                       "lba_raw"
#                     ],
#                     "default": "lba_npp",
#                     "propertyOrder": 8
#                   }}
#                 }
#             }
#         }
#     return schema


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
    with open(stdoutfn, 'w') as stdout, open(stderrfn, 'w') as stderr:
        subprocess.run(['LGPPP_LRT.py', obs_fn, config_fn], cwd=target, stdout=stdout, stderr=stderr)


def run_pipeline(observation, **config):
    pdir = os.environ['LGPPP_ROOT']
    job_id = str(uuid.uuid4())

    obs_fn = path.join(pdir, 'srm.' + job_id + '.txt')
    write_observations(observation, obs_fn)
    config_fn = path.join(pdir, 'master_setup.' + job_id + '.cfg')
    write_config(config, config_fn)

    run(pdir, obs_fn, config_fn, job_id)

    return pdir + '-' + job_id
