from flask import Blueprint, render_template

# self import

rule_blueprint = Blueprint('rule', __name__)


@rule_blueprint.route("/rule")
def rule():
    return render_template('rule.html'), 200
