from flask import render_template
from common.ConfigKeys import ConfigKeys

def register_error_handlers(app):
    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error(f"Internal server error: {e}", exc_info=True)
        
        # In development, mostra l'errore reale
        error_message = getattr(e, "original_exception", e)
        
        return render_template(
            "500.html",
            error=error_message,
            github_issue_link=ConfigKeys.Keys.GITHUB_ISSUES_LINK.value
        ), 500

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404
