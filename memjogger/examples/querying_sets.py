import sys
from memjogger.api import Handle

if __name__ == '__main__':
    api = Handle(email = sys.argv[1], password = sys.argv[2])
    result = api.get_card_sets()
    for cs in result.data['card_sets']:
        print cs['id'], cs['name']