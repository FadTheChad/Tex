async def on_message(message):
    print(message.content)

event = {
    'name': 'on_message',
    'run': on_message
}