from path import Path
from strictyaml import load
from re import compile

class Config:

    def __init__(self, path: str):
        """Create a Config Object.

        Contains configuration given by the user including penetration information,
        namespaces etc.

        Keyword Arguments:
        self                   -- This object.
        path                   -- String with the path to the config file.
        """
        self._config = load(Path(path).read_text('UTF-8')).data

    def section(self, section: str, context: dict = {}) -> dict:
        """Extract a section of the configuration.

        Check the config file for a section and replace possible variables
        with values from the context. e.g. hostnames

        Keyword Arguments:
        self                   -- This object.
        section                -- String indicating section to look for in config.
        context                -- Dict wheras the keys are possible variables to
                                  replace with the value.
        Return Value:
        Dict with section configuration
        """

        config = self._config.get(section, {})
        pattern = compile(r".*?{{ (\w+) }}.*?")

        for key, item in config.items():
            match = pattern.findall(item)
            for var in match:
                config[key] = item.replace(f"{{{{ {var} }}}}", context.get(var, f"{{{{ {var} }}}}"))

        return config
