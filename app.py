import os.path
from os import listdir
import zipfile
from time import sleep
from FeatureCloud.cli.cli import Controller
from functools import partial
import shutil
from distutils.dir_util import copy_tree


class TestApp(Controller):
    def __init__(self, app_id, ctrl_data_path, ctrl_test_path, n_clients, app_image, **kwargs):
        super().__init__(**kwargs)
        self.app_image = app_image
        self.test_id = None
        self.n_clients = n_clients
        self.path_to_extracted_data = {}
        self.results_ready = False
        self.app_id = app_id
        self.generic_dir = ""
        self.clients_path = []
        self.clients_relative_path = []
        self.results_path = ""
        self.results_relative_path = ""
        self.create_paths(ctrl_data_path, ctrl_test_path)
        self.start = partial(self.start,
                             client_dirs=self.clients_relative_path,
                             generic_dir=self.generic_dir,
                             app_image=app_image,
                             download_results=self.results_relative_path)
        self.stop = partial(self.stop, self.test_id)

    def set_id(self, test_id):
        self.test_id = test_id
        self.delete = partial(self.delete, test_id=self.test_id, what='')

    def extract_results(self, def_res_file):
        zip_files = [f for f in listdir(self.results_path) if f.endswith(".zip")]
        os.makedirs(self.results_path, exist_ok=True)
        if len(zip_files) > 1:
            print(f"Extracting the results of {self.app_image} ...")
            for zip_file in zip_files:
                client_n = int(zip_file.strip().split("client_")[-1].strip().split("_")[0])
                res_dir = f"{self.clients_path[client_n]}/{def_res_file}"
                zip_file_path = f"{self.results_path}/{zip_file}"
                if not os.path.exists(res_dir):
                    os.makedirs(res_dir, exist_ok=True)
                    print(f"Create {res_dir} directory...")
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(res_dir)
                    print(f"Extract client {client_n} to {res_dir} directory...")
            self.results_ready = True
        else:
            print(f"Looking into {self.results_path}\n"
                  f"There is no file yet!\n"
                  "We will check again later....")
            sleep(5)
            self.extract_results(def_res_file)

    def wait_until_finishes(self):
        while not self.is_finished():
            sleep(5)

    def is_finished(self):
        df = self.info(test_id=self.test_id, format='dataframe')
        return df.status.values == "finished"

    def clean_dirs(self, def_re_dir):
        for c_dir in self.clients_path:
            print(c_dir, def_re_dir)
            if os.path.exists(f"{c_dir}/{def_re_dir}"):
                print(f"Delete {c_dir}/{def_re_dir}")
                shutil.rmtree(f"{c_dir}/{def_re_dir}")
        if os.path.exists(self.results_path):
            for zip_file in os.listdir(self.results_path):
                if zip_file.endswith(".zip"):
                    print(f"Delete {self.results_path}/{zip_file}")
                    os.remove(f"{self.results_path}/{zip_file}")
        else:
            os.mkdir(self.results_path)

    def create_paths(self, ctrl_data_path, ctrl_test_path):
        self.results_relative_path = f"./results/app{self.app_id}"
        clients_relpath = [f"./app{self.app_id}/client_{c}" for c in range(self.n_clients)]
        self.clients_relative_path = ",".join(clients_relpath)
        self.clients_path = [f"{ctrl_data_path}{clients_relpath[c][1:]}" for c in
                             range(self.n_clients)]
        self.results_path = f"{ctrl_test_path}{self.results_relative_path[1:]}"
        self.generic_dir = f"./app{self.app_id}/generic"

    def copy_results(self, ctrl_data_path, dest_generic, dest_clients, default_res_name):
        for client_n, client_res in enumerate(self.clients_path):
            res_dir = f"{client_res}/{default_res_name}"
            print(f"Copy {res_dir} to {dest_clients[client_n]} ...")
            copy_tree(res_dir, dest_clients[client_n])
        copy_tree(f"{ctrl_data_path}{dest_generic[1:]}",
                  f"{ctrl_data_path}{dest_generic[1:]}")
