import datajoint as dj
import importlib
import inspect
from . import subject


schema = dj.schema()


def activate(
    genotyping_schema_name,
    subject_schema_name=None,
    create_schema=True,
    create_tables=True,
    linking_module=None,
):
    """Activate this schema.

    Args:
        genotyping_schema_name (str): schema name on the database server to
                                    activate the `genotyping` element.
        subject_schema_name (str): schema name on the database server to
                                activate the `subject` element
        create_schema (bool, optional): when True (default), create schema in the
                            database if it does not yet exist.
        create_tables (bool, optional): when True (default), create tables in the
                            database if they do not yet exist.
        linking_module (bool, optional): a module name or a module containing the
        required dependencies to activate the `subject` element:

    Dependencies:
    Upstream tables:
        Source: The source of the material/resources (e.g. allele, animal) - typically refers to the
                    vendor (e.g. Jackson Lab - JAX).
        Lab: The lab for which a particular animal belongs to.
        Protocol: The protocol applicable to a particular animal (e.g. IACUC, IRB).
        User: The user associated with a particular animal.
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
        genotyping_schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        add_objects=linking_module.__dict__,
    )


@schema
class Sequence(dj.Lookup):
    """Gene sequence information.

    Attributes:
        sequence ( varchar(32) ): Abbreviated sequence name
        base_pairs ( varchar(1024) ): Base pairs
        sequence_desc ( varchar(255) ): Description
    """

    definition = """
    sequence            : varchar(32)   # abbreviated sequence name
    ---
    base_pairs=''       : varchar(1024) # base pairs
    sequence_desc=''    : varchar(255)  # description
    """


@schema
class AlleleSequence(dj.Lookup):
    """Allele sequence information.

    Attributes:
        subject.Allele (foreign key): subject.Allele key.
        Sequence ( varchar(1024) ): Sequence key.
    """

    definition = """
    -> subject.Allele
    -> Sequence
    """


@schema
class BreedingPair(dj.Manual):
    """Information about male-female pair used for breeding.

    Attributes:
        breeding_pair ( varchar(24) ): Pair identifier.
        bp_start_date (date): Optional. Start date of breeding.
        bp_end_date (date): Option. End date of breeding.
        bp_description ( varchar(2048) ): Description of the pair.
    """

    definition = """
    -> subject.Line
    breeding_pair           : varchar(32)
    ---
    bp_start_date=null      : date
    bp_end_date=null        : date
    bp_description=''       : varchar(2048)
    """

    class Father(dj.Part):
        """Information about male breeder.

        Attributes:
            BreedingPair (foreign key): BreedingPair key.
            subject.Subject (foreign key): subject.Subject key.
        """

        definition = """
        -> master
        ---
        -> subject.Subject.proj(father="subject")
        """

    class Mother(dj.Part):
        """Information about female breeder.

        Attributes:
            BreedingPair (foreign key): BreedingPair key.
            subject.Subject (foreign key): subject.Subject key.
        """

        definition = """
        -> master
        ---
        -> subject.Subject.proj(mother="subject")
        """


@schema
class Litter(dj.Manual):
    """Information about litter (group of animals born to a breeding pair).

    Attributes:
        BreedingPair (foreign key): BreedingPair key.
        litter_birth_date (date): Birth date of litter.
        num_of_pups (tinyint): Number of animals in the litter.
        litter_notes ( varchar(255) ): Notes about the litter.
    """

    definition = """
    -> BreedingPair
    litter_birth_date       : date
    ---
    num_of_pups             : tinyint
    litter_notes=''         : varchar(255)
    """


@schema
class Weaning(dj.Manual):
    """Information about weaning (maternal separation).

    Attributes:
        Litter (foreign key): Litter key.
        weaning_date (date): Litter key.
        num_of_male (tinyint): Number of males.
        num_of_female (tinyint): Number of females.
        weaning_notes ( varchar(255) ): Notes about weaning.
    """

    definition = """
    -> Litter
    ---
    weaning_date            : date
    num_of_male             : tinyint
    num_of_female           : tinyint
    weaning_notes=''        : varchar(255)
    """


@schema
class SubjectLitter(dj.Manual):
    """Subject and its litter.

    Attributes:
        subject.Subject (foreign key): subject.Subject key.
        Litter (foreign key): Litter key.
    """

    definition = """
    -> subject.Subject
    ---
    -> Litter
    """


@schema
class Cage(dj.Lookup):
    """Cage information.

    Attributes:
        cage ( varchar(32) ): Cage identifier.
        cage_purpose ( varchar(128) ): Cage purpose.
    """

    definition = """
    cage            : varchar(32)   # cage identifier
    ---
    cage_purpose='' : varchar(128)  # cage purpose
    """


@schema
class SubjectCaging(dj.Manual):
    """Information about subject and its cage.

    Attributes:
        subject.Subject (foreign key): subject.Subject key.
        caging_datetime (datetime): Date of cage entry.
        Cage (foreign key): Cage key.
        User (foreign key): User key.
    """

    definition = """
    # record of animal caging
    -> subject.Subject
    caging_datetime     : datetime   # date of cage entry
    ---
    -> Cage
    -> User           # person associated with the cage transfer
    """


@schema
class GenotypeTest(dj.Manual):
    """Information about genotype test.

    Attributes:
        subject.Subject (foreign key): subject.Subject key.
        Sequence (foreign key): Sequence key.
        genotype_test_id (datetime): Identifier of a genotype test.
        test_result (Present or Absent): Test result.
    """

    definition = """
    -> subject.Subject
    -> Sequence
    genotype_test_id    : varchar(32)    # identifier of a genotype test
    ---
    test_result         : enum("Present", "Absent")     # test result
    """
