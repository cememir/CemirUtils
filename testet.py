from cemirutils import CemirUtilsConditions

# Sample usage of condition_collector decorator
@CemirUtilsConditions.condition_collector
def sample_condition(x):
    if x > 10:
        return "Greater than 10"
    else:
        return "10 or less"

print(sample_condition(15))