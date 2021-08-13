from .case import case, docketentry
from .record_on_appeal import (
    record_on_appeal as _record_on_appeal,
    record_on_appeal_docket_entry as _record_on_appeal_docket_entry
)
from .court_resolvers import court
from .query import query as _query
from .mutations import mutation
from .dev_helpers import dev_mutation

resolvers = [
    _query,
    mutation,
    dev_mutation,
    case,
    court,
    docketentry,
    _record_on_appeal,
    _record_on_appeal_docket_entry
]
