import time
from datetime import datetime

from cemirutils import CemirUtilsDecorators


@CemirUtilsDecorators.before_after
def test_beforeafter(data):
    print(f"1 Performing database operation with data: {data}")
    return "2 Success"

print(test_beforeafter("Muslu Y."))
