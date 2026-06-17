import click
from flask.cli import with_appcontext

from database import db
from models import User


@click.group("users")
def users_cli():
    """User management commands."""
    pass


@users_cli.command("list")
@with_appcontext
def list_users():
    click.echo(
        f"{'ID':36} {'ROLE':8} {'PROVIDER':10} {'EMAIL':40}"
    )
    click.echo("-" * 100)

    for u in User.query.order_by(User.email).all():
        click.echo(
            f"{str(u.id):36} "
            f"{u.role:8} "
            f"{u.auth_provider:10} "
            f"{u.email}"
        )