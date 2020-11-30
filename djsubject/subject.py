import datajoint as dj
from djutils.templates import SchemaTemplate


schema = SchemaTemplate()


@schema
class Strain(dj.Lookup):
    # strain of animal, C57/Bl6
    definition = """
    strain              : varchar(32)	# informal name of a strain
    ---
    strain_standard_name  : varchar(32)   # formal name of a strain
    strain_desc=''      : varchar(255)	# description of this strain
    """


@schema
class Sequence(dj.Lookup):
    definition = """
    sequence            : varchar(32)	# informal name of a sequence
    ---
    base_pairs=''       : varchar(1024)	# base pairs
    sequence_desc=''    : varchar(255)	# description
    """


@schema
class Allele(dj.Lookup):

    _Source = ...

    definition = """
    allele                      : varchar(255)    # informal name of an allele
    ---
    allele_standard_name=''     : varchar(255)	  # standard name of an allele
    """

    class Source(dj.Part):
        definition = """
        -> master
        ---
        -> master._Source
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
    line                    : varchar(32)	# informal name of a line
    ---
    line_desc=''            : varchar(2048)	# description
    target_phenotype=''     : varchar(255)	# target phenotype
    is_active               : boolean		# whether the line is in active breeding
    """

    class Allele(dj.Part):
        definition = """
        -> master
        -> Allele
        """


@schema
class Subject(dj.Manual):

    _Lab = ...
    _Protocol = ...
    _User = ...
    _Source = ...

    definition = """
    subject                 : varchar(32)
    ---
    sex                     : enum('M', 'F', 'U')	# sex
    subject_birth_date      : date			        # birth date
    subject_desc=''         : varchar(1024)
    """

    # idea here: when query the master table,
    # return part table columns if entries exist
    class Protocol(dj.Part):
        definition = """
        -> master
        -> master._Protocol
        """

    class User(dj.Part):
        definition = """
        -> master
        -> master._User
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
        -> master._Source
        """

    class Lab(dj.Part):
        definition = """
        -> master
        -> master._Lab
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
    bp_start_date=null      : date		            # start date
    bp_end_date=null        : date			        # end date
    bp_desc=''              :	varchar(2048)		# description
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
    cage            : varchar(64)   # cage identifying info
    ---
    cage_purpose='' : varchar(128)  # cage purpose
    """


@schema
class SubjectCaging(dj.Manual):

    _User = ...

    definition = """
    # record of animal caging
    -> Subject
    caging_datetime     : datetime   # date of cage entry
    ---
    -> Cage
    -> self._User           # person associated with the cage transfer
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
