import pprint
import shelve
import web

path = '/home/ypcat/cgi-bin/notify.db'

class notify:
    def GET(self):
        db = shelve.open(path)
        f = web.form.Form(
            web.form.Dropdown('site', args=db['sites'].keys(), value=db['sites'].keys()[0]),
            web.form.Textbox('email'),
            web.form.Button('register', type='submit'),
            web.form.Button('unregister', type='submit'),
        )
        dump = pprint.pformat(dict(db))
        db.close()
        return '''<h1>Update notification</h1>
        <form method="POST">%(form)s</form>
        <pre>%(db)s</pre>
        ''' % {'form':f.render(), 'db':dump}
    def POST(self):
        data = web.input()
        db = shelve.open(path, writeback=True)
        if data.email and data.site in db['sites']:
            if 'register' in data:
                db['sites'][data.site]['subscribers'][data.email] = 1
            elif 'unregister' in data and data.email in db['sites'][data.site]['subscribers']:
                del db['sites'][data.site]['subscribers'][data.email]
        db.close()
        raise web.seeother('/')

application = web.application((
    '/?', 'notify',
    ), globals())

