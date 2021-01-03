CREATE_GOAL_CALLBACK_ID = "create_goal_view_id"
CREATE_GOAL_INPUT = "create_goal_action"
CREATE_GOAL_INPUT_BLOCK = "create_goal_input_block"
CREATE_GOAL = {
    "type": "modal",
    "callback_id": CREATE_GOAL_CALLBACK_ID,
    "title": {"type": "plain_text", "text": "Create Goal"},
    "submit": {"type": "plain_text", "text": "Submit"},
    "close": {"type": "plain_text", "text": "Cancel"},
    "blocks": [
        {
            "type": "input",
            "block_id": CREATE_GOAL_INPUT_BLOCK,
            "element": {"type": "plain_text_input", "action_id": CREATE_GOAL_INPUT},
            "label": {"type": "plain_text", "text": " "},
        }
    ],
}
