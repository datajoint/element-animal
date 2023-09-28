import importlib
import inspect

import datajoint as dj

schema = dj.schema()


def activate(
    schema_name: str,
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
        Source: The source of the material/resources
                    (e.g. allele, animal) - typically refers to the
                    vendor (e.g. Jackson Lab - JAX)
        Lab: The lab for which a particular animal belongs to
        Protocol: the protocol applicable to a particular animal
                    (e.g. IACUC, IRB)
        User: the user associated with a particular animal
    """

    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(
        linking_module
    ), "The argument 'linking_module' must be a module's name or a module"

    global _linking_module
    _linking_module = linking_module

    schema.activate(
        schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        add_objects=linking_module.__dict__,
    )


@schema
class Strain(dj.Lookup):
    """Genetic strain of an animal. (e.g. C57Bl/6).

    Attributes:
        strain ( varchar(32) ): Abbreviated strain name.
        strain_standard_name ( varchar(32) ): Formal name of a strain.
        strain_desc ( varchar(255) ): Optional. Description of this strain.
    """

    definition = """
    strain                  : varchar(32)	# abbreviated strain name
    ---
    strain_standard_name    : varchar(32)   # formal name of a strain
    strain_desc=''          : varchar(255)	# description of this strain
    """


@schema
class Allele(dj.Lookup):
    """Store allele information.

    Attributes:
        allele ( varchar(32) ): Abbreviated allele name.
        allele_standard_name ( varchar(255) ): Optional. Standard name of an allele.
    """

    definition = """
    allele                    : varchar(32)  # abbreviated allele name
    ---
    allele_standard_name=''   : varchar(255) # standard name of an allele
    """

    class Source(dj.Part):
        """Source of an allele.

        Attributes:
            Allele (foreign key): Allele key.
            source_identifier ( varchar(255) ): ID of the provider.
            source_url ( varchar(255) ): Optional. URL to the source information
            expression_data_url ( varchar(255) ): Optional. Link to the expression pattern from Allen institute brain atlas.
        """

        definition = """
        -> master
        ---
        -> Source
        source_identifier=''  : varchar(255)
        source_url=''         : varchar(255) # link to the line information
        expression_data_url='': varchar(255) # link to the expression pattern from Allen institute brain atlas
        """


@schema
class Line(dj.Lookup):
    """Genetic line.

    Attributes:
        line ( varchar(32) ): Abbreviated name for the line.
        species ( varchar(64) ): Latin name preferred for NWB export.
        line_description ( varchar(2000) ): Optional. Description of the line.
        target_phenotype ( varchar(255) ): Optional. Targeted gene phenotype.
        is_active (boolean) : Whether the line is in active breeding.
    """

    definition = """
    line                : varchar(32)  # abbreviated name for the line
    ---
    species=''          : varchar(64)  # Latin name preferred for NWB export
    line_description='' : varchar(2000)
    target_phenotype='' : varchar(255)
    is_active           : boolean	   # whether the line is in active breeding
    """

    class Allele(dj.Part):
        """Allele of the line.

        Attributes:
            Line (foreign key): Line key.
            Allele (foreign key): Allele key.
        """

        definition = """
        -> master
        -> Allele
        """


@schema
class Subject(dj.Manual):
    """Animal subject information.

    Attributes:
        subject ( varchar(8) ): Subject ID.
        subject_nickname ( varchar(8) ): Subject nickname.
        sex (enum): 'M', 'F', or 'U'; Male, Female, or Unknown.
        subject_birth_date (date): Birth date of the subject.
        subject_description ( varchar(1024) ): Description of the subject.
    """

    definition = """
    subject                 : varchar(8)
    ---
    subject_nickname=''     : varchar(64)
    sex                     : enum('M', 'F', 'U')
    subject_birth_date      : date
    subject_description=''  : varchar(1024)
    """

    class Species(dj.Part):
        """Subject species as Latin binomial or NCBI taxonomic identifier.

        Attributes:
            Subject (foreign key): Primary key from Subject.
            species (str): Subject species as Latin binomial or NCBI taxonomic identifier.
        """
        
        definition = """
        -> master
        ---
        species     : varchar(32)
        """

    class Protocol(dj.Part):
        """Protocol under which this subject animal is used.

        Attributes:
            Subject (foreign key): Subject key.
            Protocol (foreign key): Protocol key.
        """

        definition = """
        -> master
        -> Protocol
        """

    class User(dj.Part):
        """Individual responsible for experiment or management of the subject.

        Attributes:
            Subject (foreign key): Subject key.
            User (foreign key): User key.
        """

        definition = """
        -> master
        -> User
        """

    class Line(dj.Part):
        """Genetic line of the subject.

        Attributes:
            Subject (foreign key): Subject key.
            Line (foreign key): Line key.
        """

        definition = """
        -> master
        ---
        -> Line
        """

    class Strain(dj.Part):
        """Genetic strain of the subject.

        Attributes:
            Subject (foreign key): Subject key.
            Strain (foreign key): Strain key.
        """

        definition = """
        -> master
        ---
        -> Strain
        """

    class Source(dj.Part):
        """Source (e.g., vendor) of the subject.

        Attributes:
            Subject (foreign key): Subject key.
            Source (foreign key): Source key.
        """

        definition = """
        -> master
        ---
        -> Source
        """

    class Lab(dj.Part):
        """Lab where the subject belongs.

        Attributes:
            Subject (foreign key): Subject key.
            Lab (foreign key): Lab key.
            subject_alias ( varchar(32) ): Alias for lab if different from id.
        """

        definition = """
        -> master
        -> Lab
        ---
        subject_alias='' : varchar(32) # alias for lab if different from id.
        """


@schema
class SubjectDeath(dj.Manual):
    """Subject death information.

    Attributes:
        Subject (foreign key): Subject key.
        date_date (date) : Death date.
    """

    definition = """
    -> Subject
    ---
    death_date  : date       # death date
    """


@schema
class SubjectCull(dj.Manual):
    """Subject culling information.

    Attributes:
        SubjectDeath (foreign key): SubjectDeath key.
        cull_method ( varchar(255) ): Optional. Culling method (e.g., cervical dislocation)
        cull_reason ( varchar(255) ): Optional. Reason for culling.
        cull_notes ( varchar(1000) ): Optional. Description of the culling.
    """

    definition = """
    -> SubjectDeath
    ---
    cull_method='': varchar(255)
    cull_reason='': varchar(255)
    cull_notes='' : varchar(1000)
    """


@schema
class Zygosity(dj.Manual):
    """Information about zygosity of a subject.

    Attributes:
        Subject (foreign key): Subject key.
        Allele (foreign key): Allele key.
        zygosity (Present or Absent or Homozygous or Heterozygous): Similarity of an allele.
    """

    definition = """
    -> Subject
    -> Allele
    ---
    zygosity : enum("Present", "Absent", "Homozygous", "Heterozygous")
    """
