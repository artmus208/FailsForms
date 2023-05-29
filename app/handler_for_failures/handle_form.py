import traceback
from flask import (
    Blueprint, flash, g, redirect, render_template, url_for, request, session
)

from .forms import ACFFormList
from .models import ArchivesCrusherFailures

from app import logger

bp = Blueprint('formhandler', __name__, url_prefix='/fail-handle')

@bp.get('')
def index():
    return "Hello, I'm handler"


@bp.get("/fail-form")
def fail_form_get():
    form:ACFFormList = ACFFormList()
    unfilled_comments = ArchivesCrusherFailures.get_unfilled_faults()
    form.make_list(unfilled_comments)
    return render_template("failures/fail_form.html", forms=form)


# INFO:
# Нужно принять старые и новые поля в форме
@bp.post("/fail-form")
def fail_form_post():
    form:ACFFormList = ACFFormList()
    unfilled_comments = ArchivesCrusherFailures.get_unfilled_faults()
    old_len, new_len = len(unfilled_comments), len(form.faults)
    need_feel_new = old_len - new_len
    form_data = request.form

    try:
        for i_old in range(old_len):
            unfilled_comments[i_old].fault = form.faults[i_old].fault.data
            unfilled_comments[i_old].save()
    except Exception:
        logger.error(f'\n{print(traceback.print_exc())}\n{e}')
        return 'There is Exc in old'
    
    try:  
        if need_feel_new:
            for i_new in range(new_len-old_len):
                name = form.faults[-1-i_new].fault.name
                list_data = form_data.getlist(name)
                logger.info(f"name:{name}|getList:{list_data}")
                new_one = ArchivesCrusherFailures(
                    crusher_id=list_data[0],
                    fail=list_data[1],
                    time_created=list_data[2]
                )
                new_one.save()
        return 'Nice'
    except Exception as e:
        logger.error(f'{traceback.print_exc()}|{e}')
        return 'there is Exception in new'
    
    
@bp.post("/fail-form-new")
def fail_form_new_post():
    form:ACFFormList = ACFFormList()
    form_data = request.form
    for f in form.faults:
        name = f.fault.name
        data_list = form_data.getlist(name)
        new_one = ArchivesCrusherFailures(
            crusher_id=data_list[0],
            fail=data_list[1],
            time_created=data_list[2]
        )
        new_one.save()
    return redirect(url_for('formhandler.fail_form_get'))
    
    
@bp.get("/journal")
def journal_get():
    journal = ArchivesCrusherFailures.get_filled_faults()
    journal_list = list()
    for j in journal:
        journal_list.append(j.as_dict())
    return render_template("failures/fail_form.html", forms=None, journal=journal_list)
