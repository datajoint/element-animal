from datetime import datetime
import json
import pynwb

from element_animal import subject


def subject_to_nwb(session_key):
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
        genotype=" x ".join(
            (subject.Line.Allele * subject.Subject.Line & subject_query).fetch("allele")
        ),
    )
