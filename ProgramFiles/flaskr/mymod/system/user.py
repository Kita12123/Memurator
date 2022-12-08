from ProgramFiles.flaskr.mymod.system.form import Form


class User:

    dic: dict[str, str | dict | Form] = {
        "MyColor": "default",
        "Department": "Sales",
        "MaxRows": 500,
        "Form": {}
    }

    def __init__(self, dic, /):
        self.dic.update(dic)
        self.dic["Form"] = Form(self.dic["Form"])

    @property
    def mycolor(self):
        return self.dic["MyColor"]

    @property
    def department(self):
        return self.dic["Department"]

    @property
    def max_rows(self):
        return self.dic["MaxRows"]

    @property
    def form(self) -> Form:
        return self.dic["Form"]

    def to_dict(self):
        return {**self.dic, **{"Form": self.dic["Form"].to_dict()}}

    def update(self, **kwarg):
        if type(kwarg.get("MyColor", "")) is not str:
            raise TypeError("MyColor arg must String!!")
        if type(kwarg.get("Department", "")) is not str:
            raise TypeError("Department arg must String!!")
        if type(kwarg.get("MaxRows", 0)) is not int:
            raise TypeError("MaxRows arg must Integer!!")
        if type(kwarg.get("Form", {})) is not dict:
            raise TypeError("Form arg must Form!!")
        self.dic.update(kwarg)
