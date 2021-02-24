from test.conftest import Target
from teamiclink.slack.commands import (
    create_goal,
    read_goals,
    uninstall,
    register_commands,
)


def test_it_registers_commands(target: Target):
    # given
    app_listeners = target.slack_handler.app._listeners
    middleware = target.slack_middleware

    # when
    register_commands(app=target.slack_handler.app, middleware=middleware)

    # then
    assert app_listeners[0].ack_function == uninstall
    assert app_listeners[0].middleware[1].func == middleware.ctx_client_id
    assert app_listeners[0].middleware[0].func == middleware.ctx_client_secret

    assert app_listeners[1].ack_function == create_goal
    assert app_listeners[1].middleware == []

    assert app_listeners[2].ack_function == read_goals
    assert app_listeners[2].middleware[0].func == middleware.ctx_goal_store
