from uuid import uuid4
from nicegui import ui, events

messages = []

@ui.refreshable
def chat_messages(own_id):
    for user_id, text, file_url in messages:
        with ui.row().classes('items-center'):
            with ui.column().classes('flex-grow'):
                ui.chat_message(text=text, sent=user_id==own_id)
                if file_url:
                    ui.link(file_url, text='Download File').classes('text-blue-500 underline')

@ui.page('/')
def index():
    user = str(uuid4())
    uploaded_file_url = None

    def send():
        nonlocal uploaded_file_url
        ui.notify('Sent!')
        messages.append((user, text.value, uploaded_file_url))
        chat_messages.refresh()
        text.value = ''
        uploaded_file_url = None

    def handle_file_upload(e: events.UploadEventArguments):
        nonlocal uploaded_file_url
        uploaded_file_url = e.url
        ui.notify('File uploaded!')

    with ui.column().classes('w-full items-stretch'):
        chat_messages(user)

    with ui.footer().classes('bg-white dark:bg-gray-800'):
        with ui.row().classes('w-full items-center'):
            text = ui.input(placeholder='message') \
                .props('rounded outlined').classes('flex-grow') \
                .on('keydown.enter', send)
            ui.button('Send', on_click=send)
            ui.upload(on_upload=handle_file_upload).props('accept=*/*').classes('max-w-full')

    ui.upload(on_upload=handle_file_upload).props('accept=image/*').classes('max-w-full')

ui.run()

