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
        roles = f"[bold blue] ID : [bold yellow]{user.role.id}[/bold yellow]" \
                f" - type : [bold green]{user.role.name}[/bold green]"
        user.password = "****" if "$argon2" in user.password else user.password
        user_table.add_row(
            str(user.id),
            user.name,
            user.email,
            roles,
            user.password, end_section=True
        )
    print("\n")
    c.print(user_table, justify="center")


def user_not_found(id):
    return Console().print(
        f"\n[blue] User with ID '[bold red]{id}[/bold red]' is "
        "'[bold red]not found[/bold red]'.\n")


def username_not_found(name):
    Console().print(
        f"\n[blue] User with name '[bold red]{name}[/bold red]' is "
        "'[bold red]not found[/bold red]'.\n")


def user_email_not_found(email):
    return Console().print(
        f"\n[blue] User with email '[bold red]{email}[/bold red]' is "
        "'[bold red]not found[/bold red]'.\n")


def login_success(name):
    message = f"\n[blue] Welcome '[bold green]{name}[/bold green]' you're logged.\n"
    Console().print(message)
    return message


def param_not_required():
    Console().print(
        "\n[blue] '[bold red]-P[/bold red]'[blue] is '[bold red]not required "
        "[/bold red]'for user creation\n")


def created_succes(user):
    Console().print(
        f"\n[bold green] '[bold blue]{user.name.upper()}[/bold blue]' created"
        " successfully.\n")


def deleted_success(id, user):
    Console().print(
        f"\n[blue] User with ID '[bold red]{id}[/bold red]', "
        f"'[bold red]{user.name.upper()}[/bold red]' "
        "has been '[bold red]deleted[/bold red]'.\n")


def invalid_pass():
    Console().print(
        "\n[blue]Password must have at least:\n"
        "[bold red]'one capital'[/bold red] from "
        "'[bold red](A-Z)'[/bold red]\n"
        "[bold red]'one lower'[/bold red] from '[bold red](a-z)'[/bold red]\n"
        "[bold red]'one number'[/bold red] from '[bold red](0-9)'[/bold red]\n"
        "[bold red]'one special char'[/bold red] from "
        "'[bold red](#?!@$%^&*-)'[/bold red]\n"
        "and at least [bold red]'8 characters'[/bold red].\n"
    )


def invalid_email():
    Console().print(
        "\n[blue]The '[bold red]Email[/bold red]' you provided is "
        "'[bold red]invalid[/bold red]'\n")


def invalid_role():
    Console().print(
        "\n'[bold red]Invalid[/bold red]'[blue] role must be ==> "
        "'[bold red]support[/bold red]' or '[bold red] commercial[/bold red]' "
        "or '[bold red]management[/bold red]'.\n")


def modification_done(user):
    Console().print(
        f"\n[bold green] '[bold blue]{user.name.upper()}[/bold blue]' "
        "successfully modified.\n")


def input_old_pass():
    check = getpass.getpass('Enter your password: ')
    return check


def new_pass():
    check = getpass.getpass('Enter or confirm  new password: ')
    return check


def wrong_pass():
    message = "\n'[bold red] You enter a wrong password[/bold red]' \n"
    Console().print(message)
    return message


def wrong_confirm_pass():
    Console().print(
        "\n[bold red '[bold red] Your confirm is wrong[/bold red]' \n")


def invalid_token():
    Console().print(
        "\n[bold green]'[bold red] Invalid Token [/bold red] please logged in "
        "again' \n")


def expired_token():
    Console().print(
        "\n[bold green]'[bold red] Token expired[/bold red] please logged in "
        "again '\n")


def logout_success():
    Console().print(
        "\n'[bold green] You have been successfully logout out[/bold green]'\n")


def logged_as(user, role):
    Console().print(
        f"\n[blue] [green]Logged as :[/green] {user}\n"
        f"\n[green] Team : [yellow]{role}[/yellow] \n", style='italic',
        justify='right')


def not_authorized():
    Console().print(
        "\n[bold green]'[bold red] You're not allowed to use this command"
        "[/bold red]'\n")


def sentry_user_created_message(user_logged, new_user):
    return f"New User {new_user.name} ID N°{new_user.id} has been created by {user_logged.name}"


def sentry_user_modification_message(user_logged, user_modified):
    return f"User {user_modified.name} ID N°{user_modified.id} has been modified by {user_logged.name}"
