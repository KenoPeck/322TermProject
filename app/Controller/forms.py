from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, IntegerField
from wtforms.validators import  DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput


from app.Model.models import Position, Research_field, Language

def get_fields():
    return Research_field.query.all()

def get_FieldName(thefield):
    return thefield.name

def get_languages():
    return Language.query.all()

def get_LanguageName(thelanguage):
    return thelanguage.name

class PositionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=50)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=1500)])
    start_date = DateField('Start Date (DD/MM/YYYY)', format='%d/%m/%Y', validators=[DataRequired()])
    end_date = DateField('End Date (DD/MM/YYYY)', format='%d/%m/%Y', validators=[DataRequired()])
    time_commitment = IntegerField('Weekly Time Commitment (Hours)', validators=[DataRequired()])
    research_fields = QuerySelectMultipleField( 'Research_field', query_factory= get_fields, get_label= get_FieldName, widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    required_languages = QuerySelectMultipleField( 'Language', query_factory= get_languages, get_label= get_LanguageName, widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    misc_requirements = TextAreaField('Other Requirements', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Submit')

class ApplicationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])