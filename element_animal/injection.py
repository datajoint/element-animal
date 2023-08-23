import importlib
import inspect

import datajoint as dj

from element_lab import lab
from . import surgery

schema = dj.Schema()

_linking_module = None


def activate(
    injection_schema_name: str,
    surgery_schema_name: str = None,
    lab_schema_name: str = None,
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

    lab.activate(
        lab_schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
    )
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
    """Virus serotype.

    Attributes:
        virus_serotype (str): Virus serotype.
    """

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
class InjectionProtocol(dj.Manual):
    """Injection device protocol.
    
    Attributes:
        protocol_id (int): Unique protocol ID.
        lab.Device (foreign key): Primary key from lab.Device.
        volume_per_pulse (float): Volume dispensed per microinjector pulse.
        injection_rate (float): Rate at which injectate is dispensed.
        interpulse_delay (float): Delay between injection pulses. Set to 0 if
        injection is a single pulse.
    """

    definition = """
    protocol_id         : int
    ---
    -> lab.Device
    volume_per_pulse    : float
    injection_rate      : float
    interpulse_delay    : float
    """


@schema
class VirusName(dj.Manual):
    """Full virus name.

    Attributes:
        virus_name (str): Full virus name. Ex: AAV1.CAG.Flex.ArchT.GFP.
        VirusSerotype (foreign key, nullable): Primary key from VirusSerotype.
    """

    definition = """
    virus_name: varchar(64)  # Full virus name. Ex: AAV1.CAG.Flex.ArchT.GFP. 
    ---
    -> [nullable] VirusSerotype
    """


@schema
class Injection(dj.Manual):
    """Information about the virus injection.

    Attributes:
        surgery.Implantation (foreign key): Primary key from
        surgery.Implantation.
        VirusName (foreign key): Primary key from VirusName.
        InjectionProtocol (foreign key): Primary key from InjectionProtocol.
        titer (str): Titer of injectate at the current injection site.
        total_volume (float): Total volume injected at the current injection 
        site.
        injection_comment (str): Comments about the virus injection. 
    """

    definition = """
    -> surgery.Implantation
    -> VirusName
    -> InjectionProtocol
    ---
    titer           : varchar(16)
    total_volume    : float
    injection_comment=''  : varchar(1024)
    """
