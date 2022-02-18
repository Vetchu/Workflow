from workflow import TestWorkFlow
from app import TestApp
from time import sleep
from functools import partial


class WorkFlow(TestWorkFlow):
    def __init__(self, controller_hosts: list, channels: list, query_intervals: list):
        super().__init__(controller_hosts, channels, query_intervals)

        self.controller_path = "/home/mohammad/PycharmProjects/FeatureCloud/data"
        self.ctrl_data_path = f"{self.controller_path}"
        self.ctrl_test_path = f"{self.controller_path}/tests"

        self.generic_dir = {}
        self.n_clients = 2
        self.TestApp = partial(TestApp,
                               n_clients=self.n_clients,
                               ctrl_data_path=self.ctrl_data_path,
                               ctrl_test_path=self.ctrl_test_path,
                               controller_host=controller_hosts[0],
                               channel=channels[0],
                               query_interval=int(query_intervals[0]))

    def register_apps(self):
        app_id = 0
        app1 = self.TestApp(app_id=app_id, app_image="featurecloud.ai/fc_cross_validation")
        self.register(app1)

        app_id += 1
        app2 = self.TestApp(app_id=app_id, app_image="featurecloud.ai/basic_rf")
        self.register(app2)

        app_id += 1
        app3 = self.TestApp(app_id=app_id, app_image="featurecloud.ai/fc_roc")
        self.register(app3)

    def run(self):
        print("Workflow execution starts ...")
        for i, app in enumerate(self.apps):
            app.clean_dirs(self.default_res_dir_name)
            id = app.start()
            app.set_id(id)
            print(f"{app.app_image}(ID: {app.test_id}) is running ...")
            app.wait_until_finishes()
            print("App execution is finished!")
            app.extract_results(self.default_res_dir_name)
            print("extracting the data...")
            while not app.results_ready:
                sleep(5)
            print("Delete the app container...")
            app.delete()
            if i < len(self.apps) - 1:
                print(f"Move {app.app_image} results to the directory of the next app({self.apps[i + 1].app_image})")
                app.copy_results(ctrl_data_path=self.ctrl_data_path,
                                 dest_clients=self.apps[i + 1].clients_path,
                                 dest_generic=self.apps[i + 1].generic_dir,
                                 default_res_name=self.default_res_dir_name)
        print("Workflow execution is finished!")
