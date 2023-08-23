import importlib
import inspect

import datajoint as dj

from . import surgery

schema = dj.Schema()

_linking_module = None


def activate(
    injection_schema_name: str,
    surgery_schema_name: str = None,
    *,
    create_schema: bool = True,
    create_tables: bool = True,
    linking_module: bool = True,
):
    """Activate this schema.

    Args:
        schema_name (str): schema name on the database server to activate the
                        `subject` element
        create_schema (bool): when True (default), create schema in the
                            database if it does not yet exist.
        create_tables (bool): when True (default), create tables in the
                            database if they do not yet exist.
        linking_module (bool): a module name or a module containing the
        required dependencies to activate the `subject` element:

    Dependencies:
    Upstream tables:
        User: the who conducted a particular surgery/implantation
    """

    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(
        linking_module
    ), "The argument 'linking_module' must be a module's name or a module"

    global _linking_module
    _linking_module = linking_module

    surgery.activate(
        surgery_schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        linking_module=linking_module,
    )
    schema.activate(
        injection_schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        add_objects=linking_module.__dict__,
    )


@schema
class VirusSerotype(dj.Lookup):
    definition = """
    virus_serotype: varchar(10)
    """
    contents = zip(
        [
            "AAV1",
            "AAV2",
            "AAV4",
            "AAV5",
            "AAV6",
            "AAV7",
            "AAV8",
            "AAV9",
            "AAV2/1",
            "AAV2/5",
            "AAV2/9",
            "AAVrg",
            "AAV/DJ",
            "pAAV",
        ]
    )


@schema
class MicroInjectionDevice(dj.Lookup):
    definition = """
    micro_injection_device: varchar(12)
    """
    contents = zip(
        [
            "Nanoject",
            "Picospritzer",
        ]
    )


@schema
class InjectionProtocol(dj.Manual):
    definition = """
    protocol_id         : int
    ---
    -> MicroInjectionDevice
    volume_per_pulse    : float
    injection_rate      : float
    interpulse_delay    : float
    """


@schema
class VirusName(dj.Manual):
    definition = """
    virus_name: varchar(64)  # Full virus name. Ex: AAV1.CAG.Flex.ArchT.GFP. 
    ---
    -> VirusSerotype
    """


@schema
class Injection(dj.Manual):
    definition = """
    -> surgery.Implantation
    -> VirusName
    -> InjectionProtocol
    ---
    titer           : varchar(16)
    total_volume    : float
    injection_comment=''  : varchar(1024)
    """
