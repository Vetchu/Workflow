import abc
from FeatureCloud.cli.cli import Controller


class TestWorkFlow(abc.ABC):
    def __init__(self, controller_hosts, channels, query_intervals):
        self.apps = []
        self.executed_app = 0
        self.controllers = [Controller(ctrl, ch, q) for ctrl, ch, q in zip(controller_hosts, channels, query_intervals)]
        self.default_res_dir_name = "AppResSults"

    @abc.abstractmethod
    def register_apps(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass

    def register(self, app):
        self.apps.append(app)
        clients_dirs = "\n\t\t".join(app.clients_path)
        msg = f"{app.app_image} app is registered:\n" \
              f"\tController: {app.controller_host}\n" \
              f"\tClient data:\n" \
              f"\t\t{clients_dirs}\n" \
              f"\tGeneric data: {app.generic_dir}\n" \
              f"\tResult dir: {app.results_path}"
        print(msg)

    def stop(self, controller_ind: int or None = None):
        if controller_ind is None:
            # Stop apps on all running controllers
            for ctrl in self.controllers:
                for test_id in ctrl.list():
                    ctrl.stop(test_id)
        else:
            # Stop apps on controller_ind controller
            for test_id in self.controllers[controller_ind].list():
                self.controllers[controller_ind].stop(test_id)

    def delete(self,  controller_ind: int or None = None):
        if controller_ind is None:
            # Delete apps on all running controllers
            for ctrl in self.controllers:
                for test_id in ctrl.list():
                    ctrl.delete(test_id)
        else:
            # Delete apps on controller_ind controller
            for test_id in self.controllers[controller_ind].list():
                self.controllers[controller_ind].delete(test_id)

    def list(self, controller_ind: int, format: str):
        print("list of apps or call apps' list methods")
        if controller_ind is None:
            ctrl_list = []
            # Get info of apps on all running controllers
            for ctrl in self.controllers:
                ctrl_list.append(ctrl.list(format))
            return ctrl_list
        return self.controllers[controller_ind].list(format)

    def info(self, format: str, controller_ind: int or None = None, ):
        info_list = []
        if controller_ind is None:
            # Get info of apps on all running controllers
            for ctrl in self.controllers:
                for test_id in ctrl.list():
                    info_list.append([ctrl.controller_host, ctrl.info(test_id, format)])
        else:
            # Get info of apps on controller_ind controller
            ctrl = self.controllers[controller_ind]
            for test_id in ctrl.list():
                info_list.append([ctrl.controller_host, ctrl.info(test_id, format)])
        return info_list

