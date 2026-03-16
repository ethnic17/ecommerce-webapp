#new blueprint
from flask import Blueprint, render_template

errors=Blueprint('errors', __name__)


#error handlers are just like routes but we use something different

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404
#in other routes, the status code is default 200

@errors.app_errorhandler(404)
def error_403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

#i wrote errors/500.html because i will make 500.html in a folder named errors in templates


