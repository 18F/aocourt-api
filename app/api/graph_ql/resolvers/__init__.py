from .case import case, docketentry
from .court_resolvers import court
from .query import query
from .mutations import mutation
from .dev_helpers import dev_mutation

resolvers = [query, mutation, dev_mutation, case, court, docketentry]
