CREATE TABLE teamiclink.slack_bot (
    id uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid (),
    team_id text UNIQUE NOT NULL,
    bot_token text NOT NULL,
    bot_id text NOT NULL,
    bot_user_id text NOT NULL,
    installed_at timestamptz NOT NULL DEFAULT NOW()
);
