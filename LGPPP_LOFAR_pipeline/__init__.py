

def give_name():
	return __name__

def give_version():
	return "0.0"

def give_argument_names():
	return ["avg_freq_step", 
			"avg_time_step", 
			"do_demix", 
			"demix_freq_step", 
			"demix_time_step", 
			"demix_sources", 
			"select_NL","parset"]

def run_pipeline(**kargs):
	print("Running pipeline", give_name(), "version", give_version())
	for k in kargs:
		print("  ", k, ":", kargs[k])

	response = "pipeline response LGPPP"
	return response