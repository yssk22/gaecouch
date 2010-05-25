import uuid

def gen_uuid(count = 1):
    # TODO: support uuid1 and sequencial uuid
    return [''.join(uuid.uuid4().__str__().split('-')) for i in range(count)]
