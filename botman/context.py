from botman.db_mgmt import fetch_conversation


def compile_context(channel, limit=600):
    """Compile context for new brain."""
    context = ''

    records = fetch_conversation(channel)
    print("this many records found:", len(list(records)))
    for record in records:
        context += '{}: {}\n\n'.format(record[2], record[0])
    context += 'UAF5C7S1Z: '

    print('Size of full context:', len(context))
    # Trim to size
    if len(context) > limit:
        start = len(context) - limit
        context = context[start:]

    print('Context being sent:')
    return context
