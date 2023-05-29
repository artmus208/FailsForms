
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, FieldList, FormField
from wtforms.validators import Length
from .models import ArchivesCrusherFailures

class TestForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    about = TextAreaField("About you")
    submit = SubmitField("Сохранить")


class ACFForm(FlaskForm):
    fault = TextAreaField("Ваша причина, сэр:",
                            validators=[Length(min=1, max=255)]
                            )
    # def __init__(self, label):
    #     self.comment.label = label

class ACFFormList(FlaskForm):
    faults = FieldList(FormField(ACFForm))
    submit = SubmitField("Отправить")

    def make_list(self, unfilled_comments):
        for i in range(len(unfilled_comments)):
            self.faults.append_entry()
            label = f"Заполните причину отказа от \
                    {unfilled_comments[i].time_created.strftime('%d.%m.%Y %H:%M')}, \
                    с номером дробилки: {unfilled_comments[i].crusher_id}"
            self.faults[i].fault.label = label             
    
    

