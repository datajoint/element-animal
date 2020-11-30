import datajoint as dj
from collections.abc import Mapping


schema = dj.schema()


def activate(database_name, create_schema=True, create_tables=True, add_objects=None):
    required_dj_classes = ("Lab", "User", "Source", "Protocol")
    assert isinstance(add_objects, Mapping) and all(
        isinstance(add_objects.get(cls, None), (dj.Manual, dj.Lookup, dj.Imported, dj.Computed))
        for cls in required_dj_classes), "Unmet requirements"
    schema.activate(database_name, create_schema=create_schema, create_tables=create_tables, add_objects=add_objects)


@schema
class Strain(dj.Lookup):
    definition = """
    # Strain of animal, e.g. C57Bl/6
    strain              : varchar(32)	# abbreviated strain name
    ---
    strain_standard_name  : varchar(32)   # formal name of a strain
    strain_desc=''      : varchar(255)	# description of this strain
    """


@schema
class Sequence(dj.Lookup):
    definition = """
    sequence            : varchar(32)	# abbreviated sequence name
    ---
    base_pairs=''       : varchar(1024)	# base pairs
    sequence_desc=''    : varchar(255)	# description
    """


@schema
class Allele(dj.Lookup):

    definition = """
    allele                      : varchar(32)    # abbreviated allele name
    ---
    allele_standard_name=''     : varchar(255)	  # standard name of an allele
    """

    class Source(dj.Part):
        definition = """
        -> master
        ---
        -> Source
        source_identifier=''        : varchar(255)    # id inside the line provider
        source_url=''               : varchar(255)    # link to the line information
        expression_data_url=''      : varchar(255)    # link to the expression pattern from Allen institute brain atlas
        """

    class Sequence(dj.Part):
        definition = """
        -> master
        -> Sequence
        """


@schema
class Line(dj.Lookup):
    definition = """
    line                    : varchar(32)	# abbreviated name for the line
    ---
    line_description=''     : varchar(2000)	
    target_phenotype=''     : varchar(255)	
    is_active               : boolean		# whether the line is in active breeding
    """

    class Allele(dj.Part):
        definition = """
        -> master
        -> Allele
        """


@schema
class Subject(dj.Manual):

    definition = """
    # Animal Subject
    subject                 : varchar(32)
    ---
    sex                     : enum('M', 'F', 'U')
    subject_birth_date      : date   
    subject_description=''  : varchar(1024)
    """

    # idea here: when query the master table,
    # return part table columns if entries exist
    class Protocol(dj.Part):
        definition = """
        -> master
        -> Protocol
        """

    class User(dj.Part):
        definition = """
        -> master
        -> User
        """

    class Line(dj.Part):
        definition = """
        -> master
        ---
        -> Line
        """

    class Strain(dj.Part):
        definition = """
        -> master
        ---
        -> Strain
        """

    class Source(dj.Part):
        definition = """
        -> master
        ---
        -> Source
        """

    class Lab(dj.Part):
        definition = """
        -> master
        -> Lab
        ---
        subject_alias=''    : varchar(32)  # alias of the subject in this lab, if different from the id
        """


@schema
class SubjectDeath(dj.Manual):
    definition = """
    -> Subject
    ---
    death_date      : date       # death date
    """


@schema
class SubjectCullMethod(dj.Manual):
    definition = """
    -> Subject
    ---
    cull_method:    varchar(255)
    """


@schema
class BreedingPair(dj.Manual):
    definition = """
    -> Line
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
        -> Subject
        """

    class Mother(dj.Part):
        definition = """
        -> master
        -> Subject
        """


@schema
class Litter(dj.Manual):
    definition = """
    # litter information, ingest when
    -> BreedingPair
    litter_birth_date       : date
    ---
    num_of_pups             : tinyint
    litter_notes=''         : varchar(255)	  # notes
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
    -> Subject
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
    -> Subject
    caging_datetime     : datetime   # date of cage entry
    ---
    -> Cage
    -> self.User           # person associated with the cage transfer
    """


@schema
class GenotypeTest(dj.Manual):
    definition = """
    -> Subject
    -> Sequence
    genotype_test_id    : varchar(32)    # identifier of a genotype test
    ---
    test_result         : enum("Present", "Absent")		# test result
    """


@schema
class Zygosity(dj.Manual):
    definition = """
    -> Subject
    -> Allele
    ---
    zygosity        : enum("Present", "Absent", "Homozygous", "Heterozygous")  # zygosity
    """
