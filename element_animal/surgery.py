import importlib
import inspect

import datajoint as dj

from . import subject

schema = dj.Schema()

_linking_module = None


def activate(
    surgery_schema_name: str,
    subject_schema_name: str = None,
    *,
    create_schema: bool = True,
    create_tables: bool = True,
    linking_module = None,
):
    """Activate this schema.

    Args:
        schema_name (str): schema name on the database server to activate the
                        `subject` element
        create_schema (bool): when True (default), create schema in the
                            database if it does not yet exist.
        create_tables (bool): when True (default), create tables in the
                            database if they do not yet exist.
        linking_module (str): A module name or a module containing the required
            dependencies to activate the `surgery` module.

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
        add_objects=_linking_module.__dict__,
    )


@schema
class CoordinateReference(dj.Lookup):
    """Coordinate reference system

    Attributes:
        reference ( varchar(60) ): Reference system (e.g., bregma, lambda, etc.)
    """

    definition = """
    reference   : varchar(32)
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
    region_name    : varchar(256)  # Brain region full name
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
        ("opto", "optogenetic perturbation"),
    )


@schema
class Implantation(dj.Manual):
    """Implantation of a device

    Attributes:
        Subject (foreign key): Subject primary key.
        implant_date (datetime): Date and time of implantation surgery.
        ImplantationType (foreign key): ImplantationType primary key.
        region_acronym ( projected attribute, varchar(32) ): Brain region
        shorthand from BrainRegion.
        hemisphere ( projected attribute, varchar(8) ): Brain region hemisphere
        from Hemisphere.
        user ( projected attribute, varchar(32) ): User who performed the surgery.
        implant_comment ( varchar(1024), optional ): Comments about the implant.
    """

    definition = """
    -> subject.Subject
    implant_date        : datetime       # surgery date
    -> ImplantationType
    -> BrainRegion.proj(target_region='region_acronym')
    -> Hemisphere.proj(target_hemisphere='hemisphere')
    ---
    -> User.proj(surgeon='user')         # surgeon
    implant_comment=''  : varchar(1024) # Comments about the implant
    """

    class Coordinate(dj.Part):
        """Coordinates of the Implantation Device.

        Attributes:
            Implantation (foreign key): Primary keys from Implantation.
            ap ( float ): In mm, Anterior/posterior; Anterior Positive.
            ap_reference (projected attribute): Coordinate reference.
            ml ( float ): In mm, medial axis; Right Positive.
            ml_reference (projected attribute): Coordinate reference.
            dv ( float ): In mm, dorso-ventral axis. Ventral negative.
            dv_reference (projected attribute): Coordinate reference.
            theta ( float, nullable ): Elevation in degrees. Rotation about ml-axis [0, 180] relative to z-axis.
            phi ( float, nullable ): Azimuth in degrees. Rotations about dv-axis [0, 360] relative to x-axis.
            beta ( float, nullable ): Rotation about shank in degrees. Rotation
            about the shank [-180, 180]. Clockwise is increasing. 0 is the probe-front facing anterior.
        """

        definition = """
        -> master
        ---
        ap=null       : float  # (mm) anterior-posterior; ref is 0
        -> [nullable] CoordinateReference.proj(ap_ref='reference')
        ml=null       : float  # (mm) medial axis; ref is 0
        -> [nullable] CoordinateReference.proj(ml_ref='reference')
        dv=null       : float  # (mm) dorso-ventral axis; ventral negative
        -> [nullable] CoordinateReference.proj(dv_ref='reference')
        theta=null    : float  # (deg) rot about ml-axis [0, 180] wrt z
        phi=null      : float  # (deg) rot about dv-axis [0, 360] wrt x
        beta=null     : float  # (deg) rot about shank [-180, 180] wrt anterior
        """
