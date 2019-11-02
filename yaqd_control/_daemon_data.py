__all__ = ["DaemonData"]


from dataclasses import asdict, dataclass, fields
from typing import Optional


@dataclass
class DaemonData:
    host: str
    port: int
    kind: str
    name: str
    config_filepath: str
    make: Optional[str] = None
    model: Optional[str] = None
    serial: Optional[str] = None

    def as_dict(self):
        return asdict(self)

    @classmethod
    def get_field_names(cls):
        return [f.name for f in fields(cls)]
