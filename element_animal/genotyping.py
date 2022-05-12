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
    """
    activate(genotyping_schema_name, subject_schema_name=None,
             create_schema=True, create_tables=True, linking_module=None)
        :param genotyping_schema_name: schema name on the database server to
                                       activate the `genotyping` element
        :param subject_schema_name: schema name on the database server to
                                    activate the `subject` element
        :param create_schema: when True (default), create schema in the
                              database if it does not yet exist.
        :param create_tables: when True (default), create tables in the
                              database if they do not yet exist.
        :param linking_module: a module name or a module containing the
         required dependencies to activate the `genotyping` element:
             Upstream tables:
                + Source: the source of the material/resources
                          (e.g. allele, animal) - typically refers to the
                          vendor (e.g. Jackson Lab - JAX)
                + Lab: the lab for which a particular animal belongs to
                + Protocol: the protocol applicable to a particular animal
                            (e.g. IACUC, IRB)
                + User: the user associated with a particular animal
    """
    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(linking_module), (
        "The argument 'dependency' must " + "be a module's name or a module"
    )

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
    definition = """
    sequence            : varchar(32)   # abbreviated sequence name
    ---
    base_pairs=''       : varchar(1024) # base pairs
    sequence_desc=''    : varchar(255)  # description
    """


@schema
class AlleleSequence(dj.Lookup):
    definition = """
    -> subject.Allele
    -> Sequence
    """


@schema
class BreedingPair(dj.Manual):
    definition = """
    -> subject.Line
    breeding_pair           : varchar(32)
    ---
    bp_start_date=null      : date
    bp_end_date=null        : date
    bp_description=''       : varchar(2048)
    """

    class Father(dj.Part):
        definition = """
        -> master
        ---
        -> subject.Subject
        """

    class Mother(dj.Part):
        definition = """
        -> master
        -> subject.Subject
        """


@schema
class Litter(dj.Manual):
    definition = """
    # litter information
    -> BreedingPair
    litter_birth_date       : date
    ---
    num_of_pups             : tinyint
    litter_notes=''         : varchar(255)    # notes
    """


@schema
class Weaning(dj.Manual):
    definition = """
    # weaning information
    -> Litter
    ---
    weaning_date            : date
    num_of_male             : tinyint
    num_of_female           : tinyint
    weaning_notes=''        : varchar(255)
    """


@schema
class SubjectLitter(dj.Manual):
    definition = """
    -> subject.Subject
    ---
    -> Litter
    """


@schema
class Cage(dj.Lookup):
    definition = """
    cage            : varchar(32)   # cage identifying info
    ---
    cage_purpose='' : varchar(128)  # cage purpose
    """


@schema
class SubjectCaging(dj.Manual):

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
    definition = """
    -> subject.Subject
    -> Sequence
    genotype_test_id    : varchar(32)    # identifier of a genotype test
    ---
    test_result         : enum("Present", "Absent")     # test result
    """
