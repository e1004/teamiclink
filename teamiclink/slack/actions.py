from typing import Type
from slack_bolt import App
from teamiclink.slack.middleware import SlackMiddleware


def delete_goal():
    pass


def register_actions(app: App, middleware: Type[SlackMiddleware]) -> None:
    action_delete_goal = app.action(
        constraints={"action_id": "delete_goal"}, middleware=[middleware.ctx_goal_store]
    )
    assert action_delete_goal
    action_delete_goal(delete_goal)
