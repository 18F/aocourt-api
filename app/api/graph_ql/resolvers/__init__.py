from .case import case, docketentry
from .query import query
from .mutations import mutation
from .dev_helpers import dev_mutation

resolvers = [query, mutation, dev_mutation, case, docketentry]
