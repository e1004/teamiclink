CREATE TABLE upt.team (
    id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    slack_team_id TEXT UNIQUE NOT NULL,
    access_token TEXT
);
