from flask.views import View
from flask import render_template, request, redirect, url_for
from flask_login import login_required
from pr.components.query import query_campaings, query_campaign_data


class HelloView(View):
    decorators = [login_required]

    def dispatch_request(self):
        db_boss, db_user = query_campaings(0), query_campaings(1)
        if request.method == 'POST':
            db_edit_page = query_campaign_data(int(request.form['submit_button']))
            return redirect(url_for('edit_campaign',
                                    camp_id=db_edit_page.camp_id))

        return render_template('main_page.html',
                               db_boss=db_boss,
                               db_user=db_user)
