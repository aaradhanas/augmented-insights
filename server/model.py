from json import JSONEncoder

class ChartInfo:
    data = {}
    data_average = 0
    columnName = ""
    type = ""

    def __init__(self, data = {}, columnName=""):
        self.data = data
        self.columnName = columnName

class AggInfo:
    title = ""
    chart = ChartInfo()
    insights = []

    def jsonDefault(object):
        return (object.title, object.insights)

# MyEncoder extends JSONEncoder
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__