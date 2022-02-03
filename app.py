import os.path
from FeatureCloud.cli import cli
from os import listdir
import zipfile
from time import sleep


class TestApp:
    def __init__(self, client_dirs, generic_dir, app_image, download_results):
        self.client_dirs = client_dirs
        self.generic_dir = generic_dir
        self.app_image = app_image
        self.download_results = download_results
        self.test_id = None
        self.n_clients = len(client_dirs)
        self.path_to_extracted_data = {}
        self.finished = False
        if not os.path.exists(self.download_results):
            os.makedirs(self.download_results, exist_ok=True)

    def set_test_id(self, test_id):
        self.test_id = test_id

    def start(self, controller_host: str, channel: str, query_interval):
        self.test_id = cli.start(controller_host, ",".join(self.client_dirs), self.generic_dir, self.app_image, channel,
                                 query_interval,
                                 self.download_results)

    def stop(self, controller_host):
        cli.stop(controller_host, self.test_id)

    def delete(self, controller_host: str, what: tuple):
        cli.delete(controller_host, self.test_id, what)

    def list(self, controller_host: str, format: str):
        cli.list(controller_host, format)

    def info(self, controller_host: str, format: str):
        cli.info(controller_host, self.test_id, format)

    def traffic(self, controller_host: str, format: str):
        cli.traffic(controller_host, self.test_id, format)

    def logs(self, controller_host: str, instance_id: str or int, from_param: str):
        cli.logs(controller_host, self.test_id, instance_id, from_param)

    def extract_results(self, results_path, clients_paths):
        zip_files = [f for f in listdir(results_path) if f.endswith(".zip")]
        os.makedirs(results_path, exist_ok=True)

        if len(zip_files) > 1:
            for zip_file in zip_files:
                client_n = int(zip_file.strip().split("client_")[-1].strip().split("_")[0])
                zip_file_path = f"{results_path}/{zip_file}"
                # ext_path = f"{client_dirs}{client_n}"
                if not os.path.exists(clients_paths[client_n]):
                    os.makedirs(clients_paths[client_n], exist_ok=True)
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(clients_paths[client_n])
            self.finished = True
        else:
            print(f"Looking into {results_path}\n"
                  f"There is no result yet!\n"
                  "We will check again later....")
            sleep(5)
            self.extract_results(results_path, clients_paths)

    def is_finished(self, controller__host):
        df = cli.info(controller__host, self.test_id, format='dataframe', echo=False)
        return df.status.values == "finished"
