import re

class CorsAllowedOriginsProperty(list):
    def __init__(self):
        super().__init__()

    def __iter__(self):
        if len(self) == 1 and self[0] == "none":
            return iter([])
        else:
            return super().__iter__()

    def add(self, string):
        return self.extend([string])

    def extend(self, collection):
        initial_size = len(self)
        for string in collection:
            if not string:
                raise ValueError("Domain cannot be an empty string or None.")
            for s in re.split(r"\s*,+\s*", string):
                if s == "all":
                    self.append("*")
                else:
                    self.append(s)

        if "none" in self:
            if len(self) > 1:
                raise ValueError("Value 'none' cannot be used with other domains")
        elif "*" in self:
            if len(self) > 1:
                raise ValueError("Values '*' or 'all' cannot be used with other domains")
        else:
            try:
                pattern = "|".join(self)
                re.compile(pattern)
            except re.error as e:
                raise ValueError("Domain values result in an invalid regex pattern") from e

        return len(self) != initial_size
