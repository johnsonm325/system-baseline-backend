from uuid import UUID

from system_baseline.exceptions import FactValidationError

FACTS_MAXSIZE = 2 ** 20  # 1 MB


def check_for_duplicate_names(facts):
    """
    check if any names are duplicated; raises an exception if duplicates are found.
    """
    names = []
    for fact in facts:
        names.append(fact["name"])
        if "values" in fact:
            check_for_duplicate_names(fact["values"])

    for name in names:
        if names.count(name) > 1:
            raise FactValidationError("name %s declared more than once" % name)


def check_for_value_values(facts):
    """
    check if any fields have "value" and "values" both defined
    """
    for fact in facts:
        if "values" in fact and "value" in fact:
            raise FactValidationError(
                "fact %s cannot have value and values defined" % fact["name"]
            )
        elif "values" in fact:
            check_for_value_values(fact["values"])


def check_for_empty_name_values(facts):
    """
    check if any names are duplicated; raises an exception if duplicates are found.
    """
    for fact in facts:
        if "values" in fact:
            check_for_empty_name_values(fact["values"])
        if "name" in fact and not fact["name"]:
            raise FactValidationError("fact name cannot be empty")
        elif "value" in fact and not fact["value"]:
            raise FactValidationError("value for %s cannot be empty" % fact["name"])


def check_facts_length(facts):
    """
    check if fact length is greater than FACTS_MAXSIZE
    """
    if len(str(facts)) > FACTS_MAXSIZE:
        raise FactValidationError(
            "attempted to save fact list over %s bytes" % FACTS_MAXSIZE
        )


def check_name_value_length(facts):
    """
    check the following lengths:
        * name is over 500 char
        * value is over 1000 char
    """
    for fact in facts:
        if "values" in fact:
            check_name_value_length(fact["values"])
        if "name" in fact and len(fact["name"]) > 500:
            raise FactValidationError(
                "fact name %s is over 500 characters" % fact["name"]
            )
        elif "value" in fact and len(fact["value"]) > 1000:
            raise FactValidationError(
                "value %s is over 1000 characters" % fact["value"]
            )


def check_uuids(baseline_ids):
    """
    helper method to test if a UUID is properly formatted. Will raise an
    exception if format is wrong.
    """
    for baseline_id in baseline_ids:
        try:
            UUID(baseline_id)
        except ValueError as e:
            raise e
