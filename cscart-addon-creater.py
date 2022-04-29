# !/usr/bin/env python
# APP Framework 1.0

import csv
import os
import sys
import shutil
import requests
from pprint import pprint


class App:
    def __init__(self):
        self.title_line = sys.argv[0]
        self.counter = 1
        self.workingDir = None

    def printCounter(self, data=None):
        print("[%04d] Porcessing: %s" % (self.counter, str(data)))
        self.counter += 1

    def initCounter(self, value=1):
        self.counter = value

    def run(self):
        self.usage()
        self.process()

    def usage(self):
        print("*" * 80)
        print("*", " " * 76, "*")
        print(" " * ((80 - 12 - len(self.title_line)) // 2),
              self.title_line,
              " " * ((80 - 12 - len(self.title_line)) // 2))
        print("*", " " * 76, "*")
        print("*" * 80)

    def input(self, notification, default=None):
        var = input(notification)

        if len(var) == 0:
            return default
        else:
            return var

    def readTxtToList(self, filename, encoding="GBK"):
        data = list()
        with open(filename, 'r+', encoding=encoding) as f:
            for row in f.readlines():
                # remove \n and \r
                data.append(row.replace('\n', '').replace('\r', ''))
        return data

    def readCsvToDict(self, filename, encoding="GBK"):
        data = list()
        with open(filename, 'r+', encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def writeCsvFromDict(self, filename, data, fieldnames=None, encoding="GBK", newline=''):
        if fieldnames is None:
            fieldnames = data[0].keys()

        with open(filename, 'w+', encoding=encoding, newline=newline) as f:
            writer = csv.DictWriter(f,
                                    fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def replaceInFile(self, filename, replace_dict):
        outlines = list()
        with open(filename, 'r') as f:
            lines = f.readlines()

            for line in lines:
                for k, v in replace_dict.items():
                    if k in line:
                        line = line.replace(k, v)  # replace k with v
                outlines.append(line)

        with open(filename, 'w') as f:
            f.writelines(outlines)

    def addSuffixToFilename(self, filename, suffix):
        filename, ext = os.path.splitext(filename)
        return filename + suffix + ext

    def getWorkingDir(self):
        return self.workingDir

    def setWorkingDir(self, wd):
        self.workingDir = wd
        return self.workingDir

    def setWorkingDirFromFilename(self, filename):
        return self.setWorkingDir(os.path.dirname(filename))

    def process(self):
        pass


class Addon:
    def __init__(self):
        self.name = None
        self.version = None
        self.description = None
        self.priority = None

    @property
    def dir_name(self):
        if self.name is None:
            raise TypeError('name is None')
        return self.name.replace(' ', '_')

    @property
    def id(self):
        if self.name is None or self.version is None:
            raise TypeError('name is None or version is None')
        return self.dir_name + "_" + self.version

    @property
    def replace_dict(self):
        return {
            '{addon_id}': self.id,
            '{addon_version}': self.version,
            '{addon_name}': self.name,
            '{addon_description}': self.description,
            '{addon_priority}': self.priority,
        }


class MyApp(App):
    def __init__(self):
        super().__init__()

        self.settings = {
            'addon_xml_sample_filename': 'addon.xml.sample',
            'addon_xml_filename': 'addon.xml',
            'dist_dir': 'dist',
        }

    def process(self):
        addon = Addon()

        # set input
        addon.name = self.input("Addon name(required): ")
        addon.version = self.input("Addon version(0.1): ", "0.1")
        addon.description = self.input("Addon description(None): ", "")
        addon.priority = self.input("Addon priority(10500): ", '10500')

        # set working directory in current directory
        self.setWorkingDirFromFilename(__file__)

        # create addon directory
        addon_dir = os.path.join(self.getWorkingDir(), self.settings['dist_dir'], addon.dir_name)
        if not os.path.exists(addon_dir):
            os.makedirs(addon_dir)

        # copy addon.xml.sample to addon directory
        addon_xml_full_path = os.path.join(addon_dir, self.settings['addon_xml_filename'])
        shutil.copy2(
            os.path.join(self.getWorkingDir(), self.settings['addon_xml_sample_filename']),
            addon_xml_full_path
        )
        # replace addon property to addon.xml
        self.replaceInFile(addon_xml_full_path, addon.replace_dict)
        sys.exit()

        # change working directory to addon directory
        self.setWorkingDir(addon_dir)


if __name__ == "__main__":
    app = MyApp()
    app.run()