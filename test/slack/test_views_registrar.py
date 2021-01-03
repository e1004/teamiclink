from test.conftest import Target
from teamiclink.slack.views import register_views, create_goal


def test_it_registers_views(target: Target):
    # given
    app_listeners = target.slack_handler.app._listeners
    middleware = target.slack_middleware

    # when
    register_views(app=target.slack_handler.app, middleware=middleware)

    # then
    assert app_listeners[0].ack_function == create_goal
    assert app_listeners[0].middleware == []
