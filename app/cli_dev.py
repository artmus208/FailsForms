import click
from flask import Blueprint
from readchar import readchar
from werkzeug.security import check_password_hash, generate_password_hash

from .handler_for_failures.models import ArchivesCrusherFailures
from . import db, logger


bp = Blueprint('dev', __name__, url_prefix='/dev')

def need_confirm(label:str):
    print(f"This is dangerous operation {label.upper()}, please, confirm your intention.")
    print('Press Y')
    c = readchar()
    if c == 'Y': return True
    else: return False 
    

@bp.cli.command('recreate-db')
def create_db():
    if need_confirm('recreate-db'):
        db.drop_all()
        db.create_all()
        db.session.commit()
        logger.warning('DB models are recreated')
        print('DB models are recreated')
    else: print('reject')
    
@bp.cli.command('seed-db')
@click.argument('crusher-id')
@click.argument('fail')
def seed_db(crusher_id, fail):
    try:
        new_one = ArchivesCrusherFailures(crusher_id=crusher_id, fail=fail)
        new_one.save()
        print("Success")
    except Exception as e:
        logger.error(str(e))
        print("Fail")
    
@bp.cli.command('get-unfilled')
def get_unfilled():
    try: 
        for m in ArchivesCrusherFailures.get_unfilled_faults():
            print(m)            
    except Exception as e:
        logger.error(e.with_traceback())
        