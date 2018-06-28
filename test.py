# export LGPPP_ROOT=$PWD/test

import LGPPP_LOFAR_pipeline
r = LGPPP_LOFAR_pipeline.run_pipeline('url1|url2', avg_freq_step=2,avg_time_step=1,do_remix=False, demix_freq_step=2, demix_time_step=2,demix_sources='CasA', select_nl=True,parset='')
print(r)
