import pickle


class ProfilesStorage:
    def __init__(self, file_path):
        self.file = file_path

    def _read_profiles(self):
        with open(file=self.file, mode="rb") as file:
            return pickle.load(file)

    def _write_profiles(self, obj):
        with open(file=self.file, mode="wb") as file:
            pickle.dump(obj, file)

    def get_profiles(self):
        return self._read_profiles()

    def del_profile(self, name):
        prof_lst = self._read_profiles()
        del_value = None
        for pfl in prof_lst:
            if pfl["name"] == name:
                del_value = pfl
        if del_value:
            prof_lst.remove(del_value)
        else:
            return "Профиля с данным именем не существует"
        self._write_profiles(prof_lst)
        return "OK"

    def add_profile(self, name, vlan, gem, srv, line):
        prof_lst = self._read_profiles()
        for pfl in prof_lst:
            if pfl["name"] == name:
                return "Профиль с таким именем уже существует"
        prof_lst.append(
            dict(name=name, vlan=vlan, gem=gem, srv=srv, line=line)
        )
        self._write_profiles(prof_lst)
        return "OK"


