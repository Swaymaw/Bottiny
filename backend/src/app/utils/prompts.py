ASSISTANT_PROMPT = "You are a Helpful AI Assistant. The user's name is {user_id}. Address them by name."

FORMAT_HINT = (
    '\n\nRespond as JSON: {"text": "<your reply>", "buttons": []}. '
    "Only fill buttons when you want the user to choose between options, "
    'each as {"id": "<short_snake_case>", "label": "<text shown to user>"}.'
)
