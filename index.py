import os
import site
site.addsitedir(os.path.dirname(__file__))

import web
import notify

web.config.debug = True # autoreload

class index:
    def GET(self):
        return 'index'

application = web.application((
    '/?', 'index',
    '/notify', notify.application,
    ), globals()).wsgifunc()

