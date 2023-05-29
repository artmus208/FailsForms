from flask import (
    Blueprint, flash, g, redirect, render_template, url_for, request, session
)

from .forms import ACFFormList
from .models import ArchivesCrusherFailures

from app import logger

bp = Blueprint('formhandler', __name__, url_prefix='/')

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
    unfilled_comments = ArchivesCrusherFailures.get_unfilled_faults()
    form = request.form
    print(form)
    return 'See console'
