from test.conftest import Target
from teamiclink.slack.actions import delete_goal, register_actions


def test_it_registers_actions(target: Target):
    # given
    app_listeners = target.slack_handler.app._listeners
    middleware = target.slack_middleware

    # when
    register_actions(app=target.slack_handler.app, middleware=middleware)

    # then
    assert app_listeners[0].ack_function == delete_goal
    assert app_listeners[0].middleware[0].func == middleware.ctx_goal_store
