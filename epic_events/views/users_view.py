from rich.console import Console
from rich.table import Table
from rich.text import Text
import getpass


def users_table(users):
    c = Console()

    user_table = Table(show_header=True, header_style="bold blue",
                       title='[bold red]Table: USERS[/bold red]')
    user_table.add_column(
        Text("ID", style="bleu", justify="center", no_wrap=True),
        justify="left", style="bold yellow",
    )
    user_table.add_column(
        Text("Name", style="blue", justify="center", no_wrap=True),
        justify="left", style="green"
    )
    user_table.add_column(
        Text("Email", style="blue", justify="center", no_wrap=True),
        justify="left", style="green"
    )
    user_table.add_column(
        Text("Backlink to Role", style="blue", justify="center", no_wrap=True),
        justify="left", style="green"
    )
    user_table.add_column(
        Text("Password", style="blue", justify="center", no_wrap=True),
        justify="left", style="red"
    )

    for user in users:
        roles = f"[bold blue] ID : [bold yellow]{user.role.id}[/bold yellow]"\
            f" - type : [bold green]{user.role.name}[/bold green]"
        user.password = "****" if "$argon2" in user.password else user.password
        user_table.add_row(
            str(user.id),
            user.name,
            user.email,
            roles,
            user.password
        )

    c.print(user_table, justify="center")


def user_not_found(id):
    Console().print(
        f"[blue] User with ID '[bold red]{id}[/bold red]' is "
        "'[bold red]not found[/bold red]'.")


def username_not_found(name):
    Console().print(
        f"[blue] User with name '[bold red]{name}[/bold red]' is "
        "'[bold red]not found[/bold red]'.")


def login_success(name):
    Console().print(
        f"[blue] Welcome '[bold green]{name}[/bold green]' you're logged.")


def param_not_required():
    Console().print(
        "[blue] '[bold red]-P[/bold red]'[blue] is '[bold red]not required "
        "[/bold red]'for user creation")


def created_succes(user):
    Console().print(
        f"[bold green] '[bold blue]{user.name.upper()}[/bold blue]'created"
        " successfully.")


def deleted_success(id, user):
    Console().print(
        f"[blue] User with ID '[bold red]{id}[/bold red]', "
        "'[bold red]{user.name.upper()}[/bold red]' "
        "has been '[bold red]deleted[/bold red]'.")


def invalid_pass():
    Console().print(
        "[blue]Password must have at least:\n"
        "[bold red]'one capital'[/bold red] from "
        "'[bold red](A-Z)'[/bold red]\n"
        "[bold red]'one lower'[/bold red] from '[bold red](a-z)'[/bold red]\n"
        "[bold red]'one number'[/bold red] from '[bold red](0-9)'[/bold red]\n"
        "[bold red]'one special char'[/bold red] from "
        "'[bold red](#?!@$%^&*-)'[/bold red]\n"
        "and at least [bold red]'8 characters'[/bold red]."
    )


def invalid_email():
    Console().print(
        "[blue]The '[bold red]Email[/bold red]' you provided is "
        "'[bold red]invalid[/bold red]'")


def invalid_role():
    Console().print(
        "'[bold red]Invalid[/bold red]'[blue] role must be ==> "
        "'[bold red]support[/bold red]' or '[bold red] commercial[/bold red]' "
        "or '[bold red]management[/bold red]'.")


def modification_done(user):
    Console().print(
        f"[bold green] '[bold blue]{user.name.upper()}[/bold blue]' "
        "successfully modified.")


def input_old_pass():
    check = getpass.getpass('Enter your password: ')
    return check


def new_pass():
    check = getpass.getpass('Enter or confirm  new password: ')
    return check


def wrong_pass():
    Console().print(
        "[bold red '[bold red] You enter a wrong password[/bold red]' ")


def wrong_confirm_pass():
    Console().print(
        "[bold red '[bold red] Your confirm is wrong[/bold red]' ")


def invalid_token():
    Console().print(
        "[bold green]'[bold red] Invalid Token [/bold red] please logged in "
        "again' ")


def expired_token():
    Console().print(
        "[bold green]'[bold red] Token expired[/bold red] please logged in "
        "again' ")


def logout_success():
    Console().print(
        "'[bold green]You have been successfully logout out[/bold green]' ")


def logged_as(user):
    Console().print(
        f"[blue] [green]Logged as :[/green] {user}", style='italic',
        justify='right')
