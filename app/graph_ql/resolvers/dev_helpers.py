from ariadne import MutationType
from app.data.dev_helpers import case_dev_util

dev_mutation = MutationType()


@dev_mutation.field("resetSeedData")
def reset_seed_data(obj, info):
    print('resetting data')
    session = info.context['request'].state.db
    case_dev_util.delete_all(session)
    case_dev_util.add_seed_cases(session)
    return True
