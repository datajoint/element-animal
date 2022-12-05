from datetime import datetime
import json
import pynwb

from .. import subject


def subject_to_nwb(session_key: dict):
    """Generate a dictionary object containing subject information.

    Args:
        session_key (dict): Key specifying one entry in element_animal.subject.Subject

    Returns:
        pynwb.file.Subject: NWB object
    """
    subject_query = subject.Subject & session_key
    subject_query = subject_query.join(subject.Subject.Line, left=True)
    subject_query = subject_query.join(subject.Subject.Strain, left=True)
    subject_query = subject_query.join(subject.Subject.Source, left=True)
    subject_info = subject_query.fetch1()

    return pynwb.file.Subject(
        subject_id=subject_info["subject"],
        sex=subject_info["sex"],
        date_of_birth=datetime.combine(
            subject_info["subject_birth_date"],
            datetime.strptime("00:00:00", "%H:%M:%S").time(),
        ),
        description=json.dumps(subject_info, default=str),
        species=(subject.Line & subject_query).fetch("species"),
        genotype=" x ".join(
            (subject.Line.Allele * subject.Subject.Line & subject_query).fetch("allele")
        ),
    )
