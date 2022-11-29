from example_wf import WorkFlow

wf = WorkFlow(controller_host="http://localhost:8000", channel="local", query_interval=5)
wf.register_apps()
wf.run()
