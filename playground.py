from werkzeug.datastructures import MultiDict

d = MultiDict(
    [('csrf_token', 'ImY0N2ZjN2Y4ZDAxZWFlZmQ2ZGE1ZTJkMzBlOGU3YTAwMzExMjMwMGYi.ZHRZhQ.76RoVgs_sS7O2Svf-McHvsr8wCI'),
     ('faults-0-fault', '123'), ('faults-1-fault', '132'), ('faults-2-fault', '123123'), 
     ('faults-3-fault', 'dfsfdfsd'), ('faults-4-fault', 'rqdfdsавыаыыв'), ('submit', 'Отправить')])

print(d['faults-2-fault'])