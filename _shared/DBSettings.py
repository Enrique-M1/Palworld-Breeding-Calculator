import os

class Settings:
    @staticmethod
    def getDBUsername():
        return os.environ['PalworldCalcUsername']

    @staticmethod
    def getDBPassword():
        return os.environ['PalworldCalcPassword']