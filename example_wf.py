from workflow import TestWorkFlow
from app import TestApp
from time import sleep
from distutils.dir_util import copy_tree


class WorkFlow(TestWorkFlow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller_path = "/home/mohammad/PycharmProjects/FeatureCloud/data"
        self.ctrl_data_path = f"{self.controller_path}"
        self.ctrl_test_path = f"{self.controller_path}/tests"

        self.generic_dir = {}
        self.n_clients = 2
        self.results_relpath = {}
        self.clients_relpath = {}
        self.clients_path = {}
        self.result_path = {}

    def register_apps(self):
        app_n = 0
        self.create_paths(app_n)
        app1 = TestApp(client_dirs=self.clients_relpath[app_n],
                       generic_dir=self.generic_dir[app_n],
                       app_image="featurecloud.ai/fc_cross_validation",
                       download_results=self.results_relpath[app_n])
        self.apps.append(app1)
        app_n += 1
        self.create_paths(app_n)
        app2 = TestApp(client_dirs=self.clients_relpath[app_n],
                       generic_dir=self.generic_dir[app_n],
                       app_image="featurecloud.ai/basic_rf",
                       download_results=self.results_relpath[app_n])
        self.apps.append(app2)
        app_n += 1
        self.create_paths(app_n)
        app3 = TestApp(client_dirs=self.clients_relpath[app_n],
                       generic_dir=self.generic_dir[app_n],
                       app_image="featurecloud.ai/fc_roc",
                       download_results=self.results_relpath[app_n])
        self.apps.append(app3)

    def run(self):
        for i, app in enumerate(self.apps):
            app.start(self.controller_host, self.channel, self.query_interval)
            while not app.is_finished(self.controller_host):
                sleep(5)
            app.extract_results(self.result_path[i], self.clients_path[i])
            while not app.finished:
                sleep(5)
            app.delete(self.controller_host, "")
            self.copy_results(i)

    def create_paths(self, app: int):
        self.results_relpath[app] = f"./results/app{app}"
        self.clients_relpath[app] = [f"./app{app}/client_{c}" for c in range(self.n_clients)]
        self.clients_path[app] = [f"{self.ctrl_data_path}{self.clients_relpath[app][c][1:]}" for c in
                                  range(self.n_clients)]
        self.result_path[app] = f"{self.ctrl_test_path}{self.results_relpath[app][1:]}"
        self.generic_dir[app] = f"./app{app}/generic"
        print(f"results relative path: {self.results_relpath[app]}")
        print(f"results full path: {self.result_path[app]}")
        print(f"clients' relative paths: {self.clients_relpath[app]}")
        print(f"Clients' full path: {self.clients_path[app]}")
        print(f"Generic path: {self.generic_dir[app]}")

        print("\n****************************\n")

    def copy_results(self, app):
        if app < len(self.clients_path) - 1:
            for client_n, client_res in enumerate(self.clients_path[app]):
                copy_tree(client_res, self.clients_path[app + 1][client_n])
            copy_tree(f"{self.ctrl_data_path}{self.generic_dir[app][1:]}",
                      f"{self.ctrl_data_path}{self.generic_dir[app + 1][1:]}")

