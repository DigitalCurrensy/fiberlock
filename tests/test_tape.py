"""The error rate must be a reading under 0.11."""
from platforms.fiberlock.src.application.session import wrap_from_pin
from platforms.fiberlock.src.application.tape import BadQber, MissingQber, qber_from_tape


class _Clock:
    def __init__(self, time_source, grade):
        self.time_source = time_source
        self.grade = grade


def test_tape_qber_wraps():
    qber = qber_from_tape({"span_id": "span-4", "qber": 0.04})
    session = wrap_from_pin("span-4", "ks-1", qber, 256, _Clock("csac", "profile_in_spec"))
    assert session.wrapped is True
    assert session.qber == 0.04


def test_missing_and_high_qber_refused():
    try:
        qber_from_tape({})
        assert False
    except MissingQber:
        pass
    try:
        qber_from_tape({"qber": 0.12})
        assert False
    except BadQber:
        pass
