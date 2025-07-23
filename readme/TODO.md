### Main Handler
- [ ] Any Message
  - [x] Add `dump_private_chat_message` to dump messages via `message.model_dump_json`
    - [ ] Add InlineButton to change dump options (`unset`, `none`, `defaults`)

### TODO
#### Infrastructure
- [ ] Kafka
  - [x] Init
  - [x] Docker service
    - [x] Healthcheck
    - [ ] CPU/MEM Usage
- [ ] Rabbit
  - [x] Init
  - [x] Docker service
    - [x] Healthcheck
    - [ ] CPU/MEM Usage
- [ ] Redis
  - [x] Init
  - [x] Docker service
    - [ ] Healthcheck
    - [ ] CPU/MEM Usage
- [ ] Postgres
  - [x] Init
  - [ ] Docker service
    - [ ] Healthcheck
    - [ ] CPU/MEM Usage
- [ ] Minio
  - [x] Init
  - [x] Docker service
    - [ ] Healthcheck
    - [ ] CPU/MEM Usage
- [ ] Aiogram
  - [x] Init

#### Functionality
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