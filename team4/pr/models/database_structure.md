# Database Structure

## Table `users`

- `users.id :: INTEGER || PK || AUTOINCREMENT` - уникальный идентификатор пользователя;
- `users.username :: TEXT || NOT NULL || UNIQUE` - `login` пользователя;
- `password_hash :: TEXT  || NOT NULL` - `hash` пароля пользователя;
- `first_name :: TEXT` - имя пользователя;
- `second_name :: TEXT` - фамилия пользователя;
- `email :: TEXT || NOT NULL` - email пользователя, проверка `regex`;
- `phone :: TEXT` - телефон пользователя;
- `updated_on :: TIMESTAMP WITHOUT TIME ZONE` - обновление данных о пользователе.

## Table `campaigns`

- `campaigns.camp_id :: INTEGER || PK || AUTOINCREMENT` - уникальный идентификатор кампании;
- `campaigns.camp_title :: TEXT || NOT NULL` - название кампании;
- `campaigns.camp_description :: TEXT` - описание кампании;
- `campaigns.camp_updated_on :: TIMESTAMP WITHOUT TIME ZONE` - обновление статуса кампании;
- `campaigns.camp_status :: BOOLEAN || NOT NULL`
    - *True*: кампания открыта;
    - *False*: кампания закрыта.

## Table `user_campaigns`

- `user_campaigns.user_id :: INTEGER || PK || FK users.id` - идентификатор пользователя;
- `user_campaigns.camp_id :: INTEGER || PK || FK campaigns.camp_id` - идентификатор пользователя в кампании;
- `user_campaigns.status_id :: INTEGER || NOT NULL`
    - 0: *создатель*
    - 1: *участник*
    - 2: *участник приглашён в кампанию*
    - 3: *участник хочет вступить в кампанию*
- `user_campaigns.updated_on :: TIMESTAMP WITHOUT TIME ZONE` - обновление статуса пользователя.

## Table `adresses`

*Адрес дома*

- `adresses.adress_id :: INTEGER || PK || AUTOINCREMENT || UNIQUE` - уникальный идентификатор дома;
- `adresses.town :: TEXT || NOT NULL` - город дома;
- `adresses.street :: TEXT || NOT NULL` - улица дома;
- `adresses.house_number :: INTEGER ` - номер дома;
- `adresses.amount_of_entrance_number :: INTEGER` - количество подъездов в доме, подъезды нумеруются `[1..amount_of_entrance_number]`;
- `adresses.amount_of_flats :: INTEGER` - количество квартир в доме, квартиры нумеруются `[1..amount_of_flats]`.

## Table `campaign_adresses`

*Cвязь кампании и адреса*

- `campaign_adresses.camp_id :: INTEGER || PK || FK campaigns.camp_id` - идентификатор кампании;
- `campaign_adresses.adress_id :: INTEGER || PK || FK adresses.adress_id` - идентификатор дома.

## Table `visits`

*Визиты участников кампаний в квартиры*

- `visit.visit_id :: INTEGER || PK || AUTOINCREMENT || UNIQUE || NOT NULL` - уникальный идентификатор визита;
- `visits.user_id :: INTEGER || PK || FK users.id` - идентификатор пользователя, делающего отзыв;
- `visits.camp_id :: INTEGER || PK || FK campaign_adresses.camp_id` - идентификатор кампании, в который пользователь состоит;
- `visits.adress_id :: INTEGER || PK || FK campaign_adresses.adress_id` - идентификатор адреса, который посетил пользователь;
- `visits.entrance_number :: INTEGER` - номер подъезда;
- `visits.flat_number :: INTEGER` - номер квартиры;
- `visits.door_open :: INTEGER` - результат прихода в квартиру:
    - `0` : дверь не открыта;
    - `1` : дверь открыта;
- `visits.visit_time :: TIMESTAMP || DEFAULT = CURRENT TIMESTAMP` - время прихода в квартиру, при пропуске - по умолчанию текущее время;
- `visits.reaction :: TEXT` - реакция жильца:
   - позитивно;
   - нейтрально;
   - негативно;
   - без реакции (если дверь не открыта)
- `visits.info :: {'name': name, 'phone': phone, 'comment': comment} | 0 ||` - удалось ли получить информацию о квартрире:
    - `0` - не удалось;
    - `dict` - заполненная информация.