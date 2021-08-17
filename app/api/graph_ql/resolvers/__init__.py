from .case_resolvers import case, docketentry
from .record_on_appeal_resolvers import (
    record_on_appeal,
    record_on_appeal_docket_entry
)
from .court_resolvers import court
from .user_resolvers import user
from .query_resolvers import query
from .mutation_resolvers import mutation
from .dev_helpers import dev_mutation

resolvers = [
    query,
    mutation,
    dev_mutation,
    case,
    court,
    user,
    docketentry,
    record_on_appeal,
    record_on_appeal_docket_entry
]
