import datajoint as dj
import importlib
import inspect


schema = dj.schema()


def activate(
    schema_name, *, create_schema=True, create_tables=True, linking_module=None
):
    """
    activate(schema_name, *, create_schema=True, create_tables=True,
             linking_module=None)
        :param schema_name: schema name on the database server to activate the
                            `subject` element
        :param create_schema: when True (default), create schema in the
                              database if it does not yet exist.
        :param create_tables: when True (default), create tables in the
                              database if they do not yet exist.
        :param linking_module: a module name or a module containing the
         required dependencies to activate the `subject` element:
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

    schema.activate(
        schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        add_objects=linking_module.__dict__,
    )


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
class Allele(dj.Lookup):

    definition = """
    allele                    : varchar(32)  # abbreviated allele name
    ---
    allele_standard_name=''   : varchar(255) # standard name of an allele
    """

    class Source(dj.Part):
        definition = """
        -> master
        ---
        -> Source
        source_identifier=''  : varchar(255) # id inside the line provider
        source_url=''         : varchar(255) # link to the line information
        expression_data_url='': varchar(255) # link to the expression pattern
                                             # from Allen institute brain atlas
        """


@schema
class Line(dj.Lookup):
    definition = """
    line                : varchar(32)  # abbreviated name for the line
    ---
    species=''          : varchar(64)  # Latin name preferred for NWB export
    line_description='' : varchar(2000)
    target_phenotype='' : varchar(255)
    is_active           : boolean	   # whether the line is in active breeding
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
    subject                 : varchar(8)
    ---
    sex                     : enum('M', 'F', 'U')
    subject_birth_date      : date
    subject_description=''  : varchar(1024)
    """

    class Protocol(dj.Part):
        definition = """
        -> master
        -> Protocol
        """

    class User(dj.Part):
        definition = """
        # Individual responsible for subject management
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
        subject_alias='' : varchar(32) # alias for lab, if different from id
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
class Zygosity(dj.Manual):
    definition = """
    -> Subject
    -> Allele
    ---
    zygosity : enum("Present", "Absent", "Homozygous", "Heterozygous")
    """
