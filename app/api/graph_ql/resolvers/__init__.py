from .case import case, docketentry
from .record_on_appeal import record_on_appeal, record_on_appeal_docket_entry
from .court_resolvers import court
from .query import query
from .mutations import mutation
from .dev_helpers import dev_mutation

resolvers = [
    query,
    mutation,
    dev_mutation,
    case,
    court,
    docketentry,
    record_on_appeal,
    record_on_appeal_docket_entry
]
