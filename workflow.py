import abc
import sys


class TestWorkFlow(abc.ABC):
    def __init__(self, controller_host, channel, query_interval):
        self.apps = []
        self.controller_host = controller_host
        self.channel = channel
        self.query_interval = query_interval
        self.executed_app = 0

    @abc.abstractmethod
    def register_apps(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass

    def register(self, app):
        self.apps.append(app)

    def stop(self):
        self.apps[self.executed_app].stop(self.controller_host)

    def delete(self):
        pass

    def list(self):
        print("list of apps or call apps' list methods")

    # def info(self, controller_host: str, test_id: str or int, format: str):
    #     cli.info(controller_host, test_id, format)
    #
    # def traffic(self, controller_host: str, test_id: str or int, format: str):
    #     cli.traffic(controller_host, test_id, format)
    #
    # def logs(self, controller_host: str, test_id: str or int, instance_id: str or int, from_param: str):
    #     cli.logs(controller_host, test_id, instance_id, from_param)


def run_workflow(wf_dir, **kwargs):
    sys.path.append(wf_dir)
    from example_wf import WorkFlow
    wf = WorkFlow(**kwargs)
    wf.register_apps()
    wf.run()
