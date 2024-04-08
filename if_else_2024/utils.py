from pydantic import StringConstraints

""" Often used constrains """
NonEmptyStr = StringConstraints(strip_whitespace=True, min_length=1)
