from flask.views import MethodView
from flask import request, render_template, redirect, url_for, flash, abort
from pr.components.query import query_check_user_in_camp, query_find_user,\
    input_values_edit_campaign, query_find_same_adress
from pr.models.user_campaigns import UserCampaigns
from flask_login import current_user
from pr.models.adresses import Adresses


# Класс отвечающий за рендер страницы с редактированием кампании
class EditCampaign(MethodView):

    def get(self, camp_id):
        adminQ, db_addresses, db_edit_page, db_users, stats_door_open, stats_reaction_get = input_values_edit_campaign(
            camp_id)
        return render_template('edit_campaign.html',
                               error='',
                               db_addresses=db_addresses,
                               db_users=db_users,
                               db_edit_page=db_edit_page,
                               adminQ=adminQ,
                               stats_door_open=stats_door_open,
                               stats_reaction_get=stats_reaction_get)

    def post(self, camp_id):
        adminQ, db_addresses, db_edit_page, db_users, stats_door_open, stats_reaction_get = input_values_edit_campaign(
            camp_id)
        # Если пользователь владеет кампанией
        if adminQ:
            # Если нажата кнопка `Добавить адрес`
            if request.form['submit_button'] == 'add_address':
                town = request.form.get('town')  # город
                street = request.form.get('street')  # улица
                house = request.form.get('house')  # номер дома
                entrance_number = request.form.get('entrance_number')  # количество подъездов
                flat_number = request.form.get('flat_number')  # количество квартир
                # проверка на отсутствие пустых ячеек
                check_correct_input = all([x is not None for x in [town, street, house, entrance_number, flat_number]])
                print(town, street, house)
                if check_correct_input:
                    if query_find_same_adress(town, street, house) is None:
                        # Добавление адреса в таблицу `adresses` / привязка адреса к кампании в таблице campaign_adresses
                        flash('Новый адрес успешно добавлен в кампанию!', 'message')
                        Adresses.add_address(town=town,
                                             street=street,
                                             house_number=house,
                                             amount_of_entrance_number=entrance_number,
                                             amount_of_flats=flat_number,
                                             camp_id=camp_id)
                    else:
                        error = 'Такой адрес уже существует'
                        return render_template('edit_campaign.html',
                                               error=error,
                                               db_addresses=db_addresses,
                                               db_users=db_users,
                                               db_edit_page=db_edit_page,
                                               adminQ=adminQ,
                                               stats_door_open=stats_door_open,
                                               stats_reaction_get=stats_reaction_get)
            elif request.form['submit_button'] == 'add_user':
                username = request.form.get('username')
                data_user = query_find_user(username)
                if data_user:
                    if query_check_user_in_camp(data_user.id, camp_id):
                        error = 'Пользователь уже в кампании'
                        return render_template('edit_campaign.html',
                                               error=error,
                                               db_addresses=db_addresses,
                                               db_users=db_users,
                                               db_edit_page=db_edit_page,
                                               adminQ=adminQ,
                                               stats_door_open=stats_door_open,
                                               stats_reaction_get=stats_reaction_get)
                    else:
                        UserCampaigns.add_user_campaigns(data_user.id,
                                                         camp_id,
                                                         1)
                        flash('Пользователь успешно добавлен в кампанию!', 'message')
                else:
                    flash('Пользователя не существует', 'error')
                    return redirect(url_for('edit_campaign',
                                            camp_id=camp_id))
            elif request.form['submit_button'] == 'Назад':
                return redirect(url_for('edit_campaign',
                                        camp_id=camp_id))
            else:
                return redirect(url_for('visit',
                                        adress_id=request.form['submit_button']))

            return redirect(url_for('edit_campaign', camp_id=camp_id))
        else:
            if request.form['submit_button'] != '':
                return redirect(url_for('visit',
                                        adress_id=request.form['submit_button']))
            else:
                abort(401)
