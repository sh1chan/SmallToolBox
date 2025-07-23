### Main Handler
- [ ] Any Message
  - [x] Add `dump_private_chat_message` to dump messages via `message.model_dump_json`
    - [ ] Add InlineButton to change dump options (`unset`, `none`, `defaults`)

### TODO
#### Infra
- [ ] Kafka
  - [x] Init
- [ ] Rabbit
  - [x] Init
- [ ] Redis
  - [x] Init
- [ ] Postgres
  - [x] Init
- [ ] Minio
  - [x] Init
- [ ] Aiogram
  - [x] Init

- [x] Move `MessageStats.is_user_admin` into `UserChats`
  - [x] Create Table
  - [ ] Add user info
- [x] Generate User Stats
  - [x] Simple Plot
    - [x] Generate pic
    - [x] Cache Generated pic filepath
      - [x] Cache will be updated for next the `hour`
    - [ ] Clear cached data (`date < curr_date - (hours=1)`)
    - [ ] Set `stats_limit`
- [x] Generate Chat Stats
  - [x] Simple Plot
    - [x] Generate pic
    - [x] Cache Generated pic filepath
      - [x] Cache will be updated for next the `hour`
    - [ ] Clear cached data (`date < curr_date - (hours=1)`)
    - [ ] Set `stats_limit`