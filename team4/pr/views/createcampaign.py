from flask.views import View
from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user
from pr.models.campaigns import Campaigns
from pr.components.query import get_camp_id_query
from pr.models.user_campaigns import UserCampaigns

# --- 1.4. NewCampaign
# Создание новой кампании


class NewCampaign(View):
    """
    Страница ./newcampaign

    ШАБЛОН ДЛЯ ЗАГРУЗКИ
    -------------------
    templates/create_campaign.html

    ОПИСАНИЕ
    -------------------

    Содержит два поля:
        - Введите название вашей кампании - campaigns.camp_title
        - Введите описание кампании - campaigns.camp_description

    Campaigns.check_unique_campaign(campaign_name)
        -- проверка на уникальность имени кампании в БД
    Campaigns.add_campaign(campaign_name, description, camp_status=True)
        -- добавление кампании по введённым данным, camp_status=True - кампания открыта
                                            :: см. models/database_structure.md
    UserCampaigns.add_user_campaigns(user_id=current_user.id, -- id пользователя
                                     camp_id=get_camp_id_query(campaign_name), -- id кампании
                                     status_id=0) -- создатель кампании
    ПЕРЕНАПРАВЛЕНИЯ
    -------------------

    ./main_page - в случае успешного добавления кампании
    ./newcapmaign - в случае ошибки добавлениея кампании

    FLASH
    -------------------

        :: flash('Название кампании уже занято', 'error') - flash-сообщение об ошибке добавления
    """
    def dispatch_request(self):
        if request.method == 'POST':
            campaign_name = request.form.get('campaign_name')
            description = request.form.get('description')
            if Campaigns.check_unique_campaign(campaign_name):
                Campaigns.add_campaign(campaign_name, description, camp_status=True)
                UserCampaigns.add_user_campaigns(user_id=current_user.id,
                                                 camp_id=get_camp_id_query(campaign_name),
                                                 status_id=0)
                return redirect(url_for('main_page'))
            else:
                flash('Название кампании уже занято', 'error')
                return redirect(url_for('newcampaign'))
        return render_template('create_campaign.html')
