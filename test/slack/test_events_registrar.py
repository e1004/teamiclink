from teamiclink.slack.middleware import SlackMiddleware
from test.conftest import Target
from teamiclink.slack.events import register_events, app_uninstalled


def test_it_registers_events(target: Target):
    # given
    app_listeners = target.slack_handler.app._listeners
    middleware = target.slack_middleware

    # when
    register_events(app=target.slack_handler.app, middleware=SlackMiddleware)

    # then
    assert app_listeners[0].ack_function == app_uninstalled
    assert app_listeners[0].middleware[0].func == middleware.ctx_install_store
