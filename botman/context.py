from botman.db_mgmt import fetch_conversation


def compile_context(channel, limit=600):
    """Compile context for new brain."""
    context = ''

    records = fetch_conversation(channel)
    for record in records:
        context += '{}: {}\n\n'.format(record[2], record[0])
    context += 'U0BOTMAN4: '
    
    # Trim to size
    if len(context) > limit:
        start = len(context) - limit
        context = context[start:]

    return context
