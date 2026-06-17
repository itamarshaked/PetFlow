import click
from flask.cli import with_appcontext

from database import db
from models import User


@click.group("users")
def users_cli():
    """User management commands."""
    pass

@click.command("make-admin")
@click.argument("email")
@with_appcontext
def make_admin(email):
    user = User.query.filter_by(email=email).first()

    if not user:
        click.secho(f"User '{email}' not found", fg="red")
        return

    if user.role == "admin":
        click.secho(f"{email} is already an admin", fg="yellow")
        return

    user.role = "admin"
    db.session.commit()

    click.secho(f"✓ {email} promoted to ADMIN", fg="green")


users_cli.add_command(make_admin)

@click.command("make-user")
@click.argument("email")
@with_appcontext
def make_user(email):
    user = User.query.filter_by(email=email).first()

    if not user:
        click.secho(f"User '{email}' not found", fg="red")
        return

    user.role = "user"
    db.session.commit()

    click.secho(f"✓ {email} changed to USER", fg="green")


users_cli.add_command(make_user)

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