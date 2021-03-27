from pr.models import db
from pr.models.campaigns import Campaigns
from pr.models.adresses import Adresses
from pr.models.campaigns import Campaigns
from pr.models.user_campaigns import UserCampaigns
from pr.models.users import Users
from pr.models.visits import Visits
from pr.models.campaign_adresses import CampaignAdresses
from flask_login import current_user
import os
import sys
import logging

logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] :: %(funcName)s: %(message)s",
    level=logging.INFO)


def campaign_query():
    """
    запрос к кампаниям чтобы вывести в main_page

    :param
    :return:
    """
    return Campaigns.query.filter()


def get_camp_id_query(title):
    return Campaigns.query.filter(Campaigns.camp_title == title).first().camp_id


def query_campaings(status):
    """
    Запрос на кампании, где залогиненный юзер создатель

    :param status: status: 0 - создатель, 1 - пользователь.
    :return:
    """
    return db.session.execute(f'''
    SELECT campaigns.camp_id, camp_title, camp_description, camp_updated_on  FROM campaigns
    INNER JOIN user_campaigns
    ON user_campaigns.camp_id=campaigns.camp_id
    WHERE user_campaigns.user_id = {current_user.id}
    AND user_campaigns.status_id = {status}
    ORDER BY campaigns.camp_updated_on DESC''').fetchall()


def query_campaign_data(id):
    """
    Получение кампании по уникальному идентификатору:

    :use:
        :: pr.views.hello.py : переход на edit_page/{id}
        :: pr.views.edit_campaign.py
    :param id: уникальный идентификатор кампании
    :return:
    """
    logging.info(id)
    return Campaigns.query.filter(Campaigns.camp_id == id).first()


def query_find_user(username):
    """
    Получение пользователя по его логину

    :use:
        :: pr.views.edit_campaign
    :param username: login_name пользователя
    :return:
    """
    logging.info(username)
    return Users.query.filter(Users.username == username).first()


def query_check_user_in_camp(user_id, camp_id):
    """
    Проверка если пользователь в кампании

    :use:
        :: pr.views.edit_campaign
    :param user_id: user_id пользователя
    :return:
    """
    logging.info(user_id)
    return UserCampaigns.query.filter(UserCampaigns.user_id == user_id,
                                      UserCampaigns.camp_id == camp_id).first()


def query_campaign_users(camp_id):
    """
    Формирование таблицы участников определённой кампании

    :use:
        :: pr.views.edit_campaign
    :param camp_id: идентификатор кампании
    :return:
    """
    return db.session.execute(f'''
    SELECT username, first_name, second_name, email, status_id FROM users
    JOIN user_campaigns
    ON users.id = user_campaigns.user_id
    and user_campaigns.camp_id = {camp_id}
    ORDER BY user_campaigns.updated_on''').fetchall()


def query_find_creator(camp_id):
    """
    Является ли пользователь создателем кампании

    :use:
        :: pr.views.edit_campaign
    :param camp_id: id_кампании
    :return:
    """
    logging.info(camp_id)
    result = UserCampaigns.query.filter(UserCampaigns.camp_id == camp_id,
                                        UserCampaigns.status_id == 0).first()
    logging.info(result)
    return result


def query_address_data(camp_id):
    """
    Адреса для определенной кампании

    :use:
        :: pr.views.edit_campaign
    :param camp_id: camp_id
    :return:
    """
    logging.info(camp_id)
    address_ids = CampaignAdresses.query.filter(CampaignAdresses.camp_id == camp_id).all()
    address_ids = [i.adress_id for i in address_ids]
    logging.info(address_ids)
    logging.info(Adresses.query.filter(Adresses.adress_id.in_(address_ids)).all())
    return Adresses.query.filter(Adresses.adress_id.in_(address_ids)).all()


def query_get_visits(adress_id):
    """
    Визиты по адресам

    :use:
        :: pr.views.edit_campaign
    :param adress_id:
    :return:
    """
    logging.info(adress_id)
    return Visits.query.filter(Visits.adress_id == adress_id).all()


def query_get_camp_id_by_address_id(adress_id):
    """
    camp_id по adress_id

    :use:
        :: pr.views.visit
    :param adress_id:
    :return:
    """
    return CampaignAdresses.query.filter(CampaignAdresses.adress_id == adress_id).first()


def query_check_username_already_in_campaign(username):
    user_ids = query_find_user(username).user_id
    return db.session.execute(
        f"select user_id from user_campaigns where username = '{user_ids}'").first()


def query_get_stats_door_open(camp_id):
    """
    Процент открытых дверей для кампании

    :use:
        :: pr.views.edit_campaign
    :param adress_id:
    :return:
    """
    res = Visits.query.filter(Visits.camp_id == camp_id).all()
    res = [i.door_open for i in res]
    logging.info(res)
    if len(res) != 0:
        res = sum(res) / len(res)
    else:
        res = 1
    return "{0:.2f}".format(100 * res)


def query_get_stats_reaction(camp_id):
    """
    Процент reaction, != None для данной кампании

    :use:
        :: pr.views.edit_campaign
    :param adress_id:
    :return:
    """
    res = Visits.query.filter(Visits.camp_id == camp_id).all()
    res = [i.reaction for i in res]
    logging.info(res)
    react = [0, 0, 0]
    total = 0
    for i in res:
        if i == 'Позитивно':
            react[0] = react[0] + 1
            total = total + 1
        elif i == 'Нейтрально':
            react[1] = react[1] + 1
            total = total + 1
        elif i == 'Негативно':
            react[2] = react[2] + 1
            total = total + 1
    logging.info(react)

    if total != 0:
        react[0] = "{0:.2f}".format(100 * react[0] / total)
        react[1] = "{0:.2f}".format(100 * react[1] / total)
        react[2] = "{0:.2f}".format(100 * react[2] / total)
    else:
        react = ['Нет данных', 'Нет данных', 'Нет данных']

    return react


def query_get_stats_door_open_for_adress(adress_id):
    """
    Процент открытых дверей для адреса

    :use:
        :: pr.views.edit_campaign
    :param adress_id:
    :return:
    """
    res = Visits.query.filter(Visits.adress_id == adress_id).all()
    res = [i.door_open for i in res]
    logging.info(res)
    if len(res) != 0:
        res = sum(res) / len(res)
    else:
        res = 1
    return "{0:.2f}".format(100 * res)


def query_get_stats_reaction_for_adress(adress_id):
    """
    Процент reaction, != None для данного адреса

    :use:
        :: pr.views.edit_campaign
    :param adress_id:
    :return:
    """
    res = Visits.query.filter(Visits.adress_id == adress_id).all()
    res = [i.reaction for i in res]
    logging.info(res)
    react = [0, 0, 0]
    total = 0
    for i in res:
        if i == 'Позитивно':
            react[0] = react[0] + 1
            total = total + 1
        elif i == 'Нейтрально':
            react[1] = react[1] + 1
            total = total + 1
        elif i == 'Негативно':
            react[2] = react[2] + 1
            total = total + 1
    logging.info(react)

    if total != 0:
        react[0] = "{0:.2f}".format(100 * react[0] / total)
        react[1] = "{0:.2f}".format(100 * react[1] / total)
        react[2] = "{0:.2f}".format(100 * react[2] / total)
    else:
        react = ['Нет данных', 'Нет данных', 'Нет данных']

    return react


def query_get_stats_flats_visited(adress_id):
    """
    Процент посещенных квартир для адреса

    :use:
        :: pr.views.visit
    :param adress_id:
    :return:
    """
    amount_of_flats = Adresses.query.filter(Adresses.adress_id == adress_id).all()
    amount_of_flats = [i.amount_of_flats for i in amount_of_flats]

    res = Visits.query.filter(Visits.adress_id == adress_id).all()
    res = [i.door_open for i in res]
    logging.info(res)
    if len(res) != 0:
        res = sum(res) / amount_of_flats[0]
    else:
        res = 0
    return "{0:.2f}".format(100 * res)


def query_get_flat_number(adress_id):
    """
    Максимальный номер квартиры

    :use:
        :: pr.views.visit
    :param adress_id:
    :return:
    """
    res = Adresses.query.filter(Adresses.adress_id == adress_id).all()
    entrance = [i.amount_of_entrance_number for i in res]
    flat = [i.amount_of_flats for i in res]
    if len(entrance) != 0:
        return [entrance[0], flat[0]]
    else:
        return 0


def adress_info_by_adress_id(adress_id):
    return Adresses.query.filter(Adresses.adress_id == adress_id).first()


def input_values_edit_campaign(camp_id):
    # проверка на владение кампанией
    adminQ = True if current_user.id == query_find_creator(camp_id).user_id else False
    # Адреса кампании
    db_addresses = reversed(query_address_data(camp_id))
    # Название кампании
    db_edit_page = query_campaign_data(camp_id)
    # Пользователи в кампании
    db_users = query_campaign_users(camp_id)
    # Статистика по открытым дверям
    stats_door_open = query_get_stats_door_open(camp_id)
    # Статистика по отзывам
    stats_reaction_get = query_get_stats_reaction(camp_id)
    return adminQ, db_addresses, db_edit_page, db_users, stats_door_open, stats_reaction_get

def query_find_same_adress(town, street, house):
    """
    Проверка на наличие такого же адреса

    :use:
        :: pr.views.edit_campaign
    :param camp_id: id_кампании
    :return:
    """
    result = Adresses.query.filter(Adresses.town == town,
                                   Adresses.street == street,
                                   Adresses.house_number == house).first()
    return result
