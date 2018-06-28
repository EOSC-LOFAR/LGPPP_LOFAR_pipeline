import tempfile
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


def write_observations(observation, target):
    srm_uris = observation.split('|')
    fn = path.join(target, 'srm.txt')

    with open(fn, 'w') as f:
        for srm_uri in srm_uris:
            f.write(srm_uri + '\n')


def write_config(config, target):
    fn = path.join(target, 'master_setup.cfg')
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


def run(target):
    stdoutfn = path.join(target, 'stdout.txt')
    stderrfn = path.join(target, 'stderr.txt')
    with open(stdoutfn, 'w') as stdout, open(stderrfn, 'w') as stderr:
        subprocess.run(['LGPPP_LRT.py', 'srm.txt', 'master_setup.cfg'], cwd=target, stdout=stdout, stderr=stderr)


def run_pipeline(observation, **config):
    mydir = tempfile.mkdtemp()

    write_observations(observation, mydir)
    write_config(config, mydir)

    run(mydir)

    return mydir
