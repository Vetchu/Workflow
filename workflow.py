import abc
from FeatureCloud.cli.cli import Controller


class TestWorkFlow(abc.ABC):
    """ The abstract TestWorkFlow class to cover basic functionalities
        for FeatureCloud workflow.
        Non-linear streams
    Attributes:
    -----------
        apps: list
            List of instances of TestApp in the workflow
        executed_app: int
            Indicator of the executed app
            Default = 0
        controllers: list
            list of instances of Controller class
        default_res_dir_name: str
            the dir-name of apps' results
    Methods:
    --------
        register_apps():
        run():
        register(app):
        stop(controller_ind):
        delete(controller_ind):
        list(controller_ind, format):
        info(format, controller_ind):
    """

    def __init__(self, controller_hosts: list, channels: list, query_intervals: list):
        self.apps = []
        self.executed_app = 0
        self.controllers = [Controller(ctrl, ch, q) for ctrl, ch, q in zip(controller_hosts, channels, query_intervals)]
        self.default_res_dir_name = "AppResSults"

    @abc.abstractmethod
    def register_apps(self):
        """ Abstract method tha should be implemented
         by developers to register apps into the workflow.

        """

    @abc.abstractmethod
    def run(self):
        """ Abstract method tha should be implemented
            by developers to run the workflow.
        """

    def register(self, app):
        """ Adding TestApp instance to the app list
            and logging the apps attributes.

        Parameters
        ----------
        app: TestApp
            app instance to be registered.

        """
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
        """ Stop all tests in the specified controller or all of them.

        Parameters
        ----------
        controller_ind: int or None
            non-negative integer as an index of target controller
            or None for all controller

        """
        if controller_ind is None:
            # Stop apps on all running controllers
            for ctrl in self.controllers:
                for test_id in ctrl.list():
                    ctrl.stop(test_id)
        elif self.controller_exist(controller_ind):
            # Stop apps on controller_ind controller
            for test_id in self.controllers[controller_ind].list():
                self.controllers[controller_ind].stop(test_id)

    def delete(self, controller_ind: int or None = None):
        """ Delete all tests in the specified controller or all of them.

        Parameters
        ----------
        controller_ind: int or None
            non-negative integer as an index of target controller
            or None for all controller

        """
        if controller_ind is None:
            # Delete apps on all running controllers
            for ctrl in self.controllers:
                for test_id in ctrl.list():
                    ctrl.delete(test_id)
        elif self.controller_exist(controller_ind):
            # Delete apps on controller_ind controller
            for test_id in self.controllers[controller_ind].list():
                self.controllers[controller_ind].delete(test_id)

    def list(self, controller_ind: int, format: str):
        """ list all tests in the specified controller or all of them.

        Parameters
        ----------
        controller_ind: int or None
            non-negative integer as an index of target controller
            or None for all controller

        """

        print("list of apps or call apps' list methods")
        if controller_ind is None:
            ctrl_list = []
            # Get info of apps on all running controllers
            for ctrl in self.controllers:
                ctrl_list.append(ctrl.list(format))
            return ctrl_list
        elif self.controller_exist(controller_ind):
            return self.controllers[controller_ind].list(format)

    def info(self, format: str, controller_ind: int or None = None):
        """ info of all tests in the specified controller or all of them.

        Parameters
        ----------
        controller_ind: int or None
            non-negative integer as an index of target controller
            or None for all controller

        """

        info_list = []
        if controller_ind is None:
            # Get info of apps on all running controllers
            for ctrl in self.controllers:
                for test_id in ctrl.list():
                    info_list.append([ctrl.controller_host, ctrl.info(test_id, format)])
        elif self.controller_exist(controller_ind):
            # Get info of apps on controller_ind controller
            ctrl = self.controllers[controller_ind]
            for test_id in ctrl.list():
                info_list.append([ctrl.controller_host, ctrl.info(test_id, format)])
        return info_list

    def controller_exist(self, controller_ind):
        """ Check either the controller index is valis or not.

        Parameters
        ----------
        controller_ind

        """
        if 0 <= controller_ind < len(self.controllers):
            return True
        print(f"Value error: Controller index is out of range."
              f"The controller index of {controller_ind} is out of list."
              f"Controller indices: [{list(range(len(self.controllers)))}]")
        return False

