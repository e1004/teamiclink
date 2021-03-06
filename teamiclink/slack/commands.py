import logging
from teamiclink.slack.model import Goal
from teamiclink.slack.store_goal import GoalStore
from teamiclink.slack.view_goal_create import CREATE_GOAL
from teamiclink.slack.middleware import SlackMiddleware
from slack_bolt import Ack, App, Say
from slack_sdk import WebClient
from slack_bolt.context import BoltContext
from typing import Any, Dict, Type

LOG = logging.getLogger(__name__)


def create_goal(ack: Ack, client: WebClient, body: Dict[str, Any]):
    ack()
    LOG.info("/create_goal")
    client.views_open(trigger_id=body["trigger_id"], view=CREATE_GOAL)


def make_goal_block(goal: Goal):
    return {
        "type": "section",
        "text": {"type": "plain_text", "text": f"{goal.content}"},
        "accessory": {
            "value": str(goal.id),
            "action_id": "delete_goal",
            "type": "button",
            "text": {"type": "plain_text", "text": "Delete"},
            "style": "danger",
            "confirm": {
                "title": {"type": "plain_text", "text": "Are you sure?"},
                "text": {
                    "type": "plain_text",
                    "text": f'Delete "{goal.content}"?',
                },
                "confirm": {"type": "plain_text", "text": "Confirm"},
                "deny": {"type": "plain_text", "text": "Cancel"},
                "style": "danger",
            },
        },
    }


def read_goals(ack: Ack, say: Say, context: BoltContext):
    ack()
    goal_store: GoalStore = context[SlackMiddleware.GOAL_STORE_KEY]
    goals = goal_store.read_goals(slack_team_id=context["team_id"])
    LOG.info(f"/read_goals: {goals}")
    if goals:
        say(text="", blocks=[make_goal_block(goal=goal) for goal in goals])
    else:
        say(text="No goals")


def uninstall(ack: Ack, client: WebClient, context: BoltContext):
    ack()
    LOG.info("/uninstalling")
    client.apps_uninstall(
        client_id=context[SlackMiddleware.CLIENT_ID_KEY],
        client_secret=context[SlackMiddleware.CLIENT_SECRET_KEY],
    )


def register_commands(app: App, middleware: Type[SlackMiddleware]):
    cmd_uninstall = app.command(
        command="/teamiclink-uninstall",
        middleware=[middleware.ctx_client_secret, middleware.ctx_client_id],
    )
    assert cmd_uninstall
    cmd_uninstall(uninstall)

    cmd_create_goal = app.command(command="/t-goal")
    assert cmd_create_goal
    cmd_create_goal(create_goal)

    cmd_read_goals = app.command(
        command="/t-goals", middleware=[middleware.ctx_goal_store]
    )
    assert cmd_read_goals
    cmd_read_goals(read_goals)
