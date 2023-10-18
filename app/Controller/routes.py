from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from config import Config

from app import db
from app.Model.models import Position
from app.Controller.forms import PositionForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET', 'POST'])
@bp_routes.route('/index', methods=['GET', 'POST'])
def index():
    positions = Position.query.order_by(Position.start_date.desc())
    focused_position = Position.query.order_by(Position.start_date.desc()).first()
    return render_template('student_homepage.html', title="Research Portal", positions=positions, position = focused_position)

@bp_routes.route('/view/<position_id>', methods=['POST'])
def view(position_id):
    positions = Position.query.order_by(Position.start_date.desc())
    theposition = Position.query.filter_by(id=position_id).first()
    return render_template('student_homepage.html', title="Research Portal", positions=positions, position = theposition)


@bp_routes.route('/new_position', methods=['GET', 'POST'])
def new_position():
    pForm = PositionForm()
    if pForm.validate_on_submit():
        newPosition = Position(title = pForm.title.data, description = pForm.description.data, start_date = pForm.start_date.data, end_date = pForm.end_date.data, time_commitment = pForm.time_commitment.data, misc_requirements = pForm.misc_requirements.data)
        for f in pForm.research_fields.data:
            newPosition.research_fields.append(f)
        for l in pForm.required_languages.data:
            newPosition.language_experience.append(l)
        db.session.add(newPosition)
        db.session.commit()
        flash('New Research Position "' + newPosition.title + '" has been created')
        return redirect(url_for('routes.index'))
    else:
        pass
    return render_template('new_position.html', form=pForm)