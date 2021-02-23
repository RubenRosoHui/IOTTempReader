from flask import render_template, Flask, send_file, send_from_directory, request, url_for, redirect, Blueprint

downloads = Blueprint("downloads", __name__, template_folder="templates")

#When routed to logs
@downloads.route('/<path:path>')
def downloadLogs(path):
    return send_from_directory("/home/pi/TPJPro/web/downloads", path, as_attachment=True, cache_timeout=0)