from flask.views import MethodView
from flask import request, render_template, redirect, url_for, flash
from pr.models.visits import Visits
from flask_login import current_user
from pr.components.query import query_get_flat_number, query_get_visits, \
    query_get_stats_flats_visited, query_get_camp_id_by_address_id, \
    query_get_stats_door_open_for_adress, \
    query_get_stats_reaction_for_adress, \
    adress_info_by_adress_id
import datetime


# Просмотр и добавление посещений одного адреса


class VisitsView(MethodView):

    def get(self, adress_id):
        db_visits = query_get_visits(adress_id)
        stats_door_open = query_get_stats_door_open_for_adress(adress_id)
        stats_reaction_get = query_get_stats_reaction_for_adress(adress_id)
        stats_flats_visited = query_get_stats_flats_visited(adress_id)
        current_adress = adress_info_by_adress_id(adress_id)
        return render_template('visits.html',
                               error='',
                               stats_flats_visited=stats_flats_visited,
                               db_visits=db_visits,
                               stats_door_open=stats_door_open,
                               stats_reaction_get=stats_reaction_get, current_adress=current_adress)

    def post(self, adress_id):
        if request.form['submit_button'] == 'add_visit':
            door_open = request.form.get('door_open')
            visit_date = request.form.get('visit_time')
            visit_time = request.form.get('time_of')
            reaction = request.form.get('reaction')
            entrance_number = request.form.get('entrance_number')
            flat_number = request.form.get('flat_number')
            info = request.form.get('info')
            db_visits = query_get_visits(adress_id)
            stats_door_open = query_get_stats_door_open_for_adress(adress_id)
            stats_reaction_get = query_get_stats_reaction_for_adress(adress_id)
            stats_flats_visited = query_get_stats_flats_visited(adress_id)
            current_adress = adress_info_by_adress_id(adress_id)
            if query_get_flat_number(adress_id)[0] < int(entrance_number):
                return render_template('visits.html',
                                       error='Невалидный номер подъезда',
                                       stats_flats_visited=stats_flats_visited,
                                       db_visits=db_visits,
                                       stats_door_open=stats_door_open,
                                       stats_reaction_get=stats_reaction_get,
                                       current_adress=current_adress)

            if query_get_flat_number(adress_id)[1] < int(flat_number):
                return render_template('visits.html',
                                       error='Невалидный номер квартиры',
                                       stats_flats_visited=stats_flats_visited,
                                       db_visits=db_visits, stats_door_open=stats_door_open,
                                       stats_reaction_get=stats_reaction_get,
                                       current_adress=current_adress)
            if door_open == "Дверь открыли":
                door_open = 1
            else:
                door_open = 0
            if door_open == 0:
                reaction = ''
            camp_id = query_get_camp_id_by_address_id(adress_id).camp_id
            if visit_date == '' or visit_date >= datetime.datetime.now().strftime("%Y-%m-%d"):
                visit_date = datetime.datetime.now().strftime("%Y-%m-%d")
            if visit_time == '' or visit_time >= datetime.datetime.now().strftime("%H:%M"):
                visit_time = datetime.datetime.now().strftime("%H:%M")
            full_time = visit_date + ' ' + visit_time
            Visits.add_visit(current_user.id,
                             camp_id,
                             adress_id,
                             entrance_number,
                             flat_number,
                             door_open,
                             full_time,
                             reaction,
                             info)
            flash(f'Добавлено новое посещение в квартиру {flat_number}, подъезд {entrance_number}', 'message')
        elif request.form['submit_button'] == 'back':
            return redirect(url_for('edit_campaign',
                                    camp_id=query_get_camp_id_by_address_id(adress_id).camp_id))
        else:
            return redirect(url_for('visit', adress_id=adress_id))
        return redirect(url_for('visit', adress_id=adress_id))
