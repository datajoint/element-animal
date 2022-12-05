import datajoint as dj
import importlib
import inspect
from . import subject

schema = dj.Schema()

_linking_module = None


def activate(
    surgery_schema_name: str,
    subject_schema_name: str = None,
    *,
    create_schema: bool = True,
    create_tables: bool = True,
    linking_module: bool = True
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

    subject.activate(
        subject_schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        linking_module=linking_module,
    )
    schema.activate(
        surgery_schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        add_objects=linking_module.__dict__,
    )


@schema
class CoordinateReference(dj.Lookup):
    """Coordinate reference system

    Attributes:
        reference ( varchar(60) ): Reference system (e.g., bregma, lambda, etc.)
    """

    definition = """
    reference   : varchar(60)
    """
    contents = zip(
        ["bregma", "lambda", "dura", "skull_surface", "sagittal_suture", "sinus"]
    )


@schema
class BrainRegion(dj.Manual):
    """Brain region of a given surgery

    Attributes:
        region_acronym ( varchar(32) ) : Brain region shorthand
        region_name ( varchar(128) ) : Brain region full name
    """

    definition = """
    region_acronym : varchar(32)   # Brain region shorthand
    ---
    region_name    : varchar(128)  # Brain region full name
    """


@schema
class Hemisphere(dj.Lookup):
    """Brain region hemisphere

    Attributes:
        hemisphere ( varchar(8) ): Brain region hemisphere (e.g., left, right, middle)
    """

    definition = """
    hemisphere: varchar(8) # Brain region hemisphere
    """

    contents = zip(["left", "right", "middle"])


@schema
class ImplantationType(dj.Lookup):
    """Type of implantation

    Attributes:
        implant_type ( varchar(16) ): Short name for type of implanted device
        implant_description ( varchar(32) ): Full description for implanted device
    """

    definition = """
    implant_type        : varchar(16) # Short name for type of implanted device
    ---
    implant_description : varchar(32) # Full description for implanted device
    """

    contents = (
        ("ephys", "electophysiology"),
        ("fiber", "fiber photometry"),
        ("opto", "optogenetic pertubation"),
    )


@schema
class Implantation(dj.Manual):
    """Implantation of a device

    WRT: With Respect To

    Attributes:
        Session (foreign key): Session primary key
        location_id (int): ID of of brain location
        ap ( decimal(6, 3) ): In um, Anterior/posterior; Anterior Positive
        ap_reference (projected attribute): Coordinate reference
        ml ( decimal(6, 3) ): In um, medial axis; Right Positive
        ml_reference (projected attribute): Coordinate reference
        dv ( decimal(6, 3) ): In um, dorso-ventral axis. Ventral negative
        dv_reference (projected attribute): Coordinate reference
        theta ( decimal(6, 3), nullable ): Elevation in degrees.
            Rotation about ml-axis [0, 180] WRT Z
        phi ( decimal(6, 3), nullable ): Azimuth in degrees.
            Rotations about dv-axis [0, 360] WRT X
        beta ( decimal(6, 3), nullable ): Rotation about shank in degrees.
            Rotation about the shank [-180, 180]. Clockwise is increasing.
            0 is the probe-front facing anterior
    """

    definition = """
    -> subject.Subject
    implant_date  : datetime       # surgery date
    -> ImplantationType
    -> BrainRegion                 # targeted brain region for this implantation
    -> Hemisphere                  # targeted hemisphere for this implantation
    ---
    -> User.proj(surgeon='user')   # surgeon
    ap            : decimal(6, 3)  # (um) anterior-posterior; ref is 0
    -> CoordinateReference.proj(ap_ref='reference')
    ml            : decimal(6, 3)  # (um) medial axis; ref is 0
    -> CoordinateReference.proj(ml_ref='reference')
    dv            : decimal(6, 3)  # (um) dorso-ventral axis; ventral negative
    -> CoordinateReference.proj(dv_ref='reference')
    theta=null    : decimal(6, 3)  # (deg) rot about ml-axis [0, 180] wrt z
    phi=null      : decimal(6, 3)  # (deg) rot about dv-axis [0, 360] wrt x
    beta=null     : decimal(6, 3)  # (deg) rot about shank [-180, 180] wrt anterior
    """
