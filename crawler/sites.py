from json import load as load_json
from pathlib import Path
from os import sep

from crawler.algorithms import Crawler

dir_path = str(Path().absolute()) + sep

class Sites():

    datasets_dir = dir_path + sep + "datasets" + sep 

    def __init__(self):
        self.__sites = []

        if not Path(self.datasets_dir).is_dir():
            Path(self.datasets_dir).mkdir(exist_ok=True)

        for site in self.get_json_file():
            self.__sites.append(Site(site[0],site[1]))


    def get_json_file(self):
        with open(dir_path + "sites.json", 'r') as file:
            json_file = load_json(file)
            
        sites = []
        for site in json_file.items():
            sites.append([site[0],site[1]])

        return sites


class Site():
    def __init__(self, name, args):
        self.__name = name
        self.__args = args

        self.__crawler = Crawler(**self.__args[0])

        self.process()

        self.__crawler.get_dataframe().to_json(
            Sites.datasets_dir + self.__name + ".json",
            orient = "records",
            lines = True,
            force_ascii = False
        )
    
    def process(self):
        self.__crawler.set_requests(**self.__args[1])
        self.__crawler.set_raw_data(**self.__args[2])
        self.__crawler.set_data_frame(**self.__args[3])

    def get_name(self):
        return self.__name
    
    def get_args(self):
        return self.__args