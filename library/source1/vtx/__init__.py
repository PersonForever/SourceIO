from pathlib import Path
from typing import BinaryIO, Union

from ...utils.byte_io_mdl import ByteIO
from .v6.vtx import Vtx as Vtx6
from .v7.vtx import Vtx as Vtx7


def open_vtx(filepath_or_object: Union[Path, str, BinaryIO, ByteIO]):
    reader = ByteIO(filepath_or_object)
    version = reader.read_int32()
    reader.file = None
    del reader
    if version == 6:
        return Vtx6(filepath_or_object)
    elif version == 7:
        return Vtx7(filepath_or_object)
