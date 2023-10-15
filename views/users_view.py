from rich.console import Console
from rich.table import Table
from rich.text import Text

import getpass


def users_table(users, table):
    c = Console()

    user_table = Table(show_header=True, header_style="bold blue",
                       title=f'[bold red]Table: {table.upper()}[/bold red]')
    user_table.add_column(
        Text("ID", style="bleu", justify="center", no_wrap=True), justify="left", style="green",
    )
    user_table.add_column(
        Text("Name", style="blue", justify="center", no_wrap=True), justify="left", style="green"
    )
    user_table.add_column(
        Text("Email", style="blue", justify="center", no_wrap=True), justify="left", style="green"
    )
    user_table.add_column(
        Text("Role", style="blue", justify="center", no_wrap=True), justify="left", style="green"
    )
    user_table.add_column(
        Text("Password", style="blue", justify="center", no_wrap=True), justify="left", style="red"
    )

    for user in users:
        user.password = "****" if "$argon2" in user.password else user.password
        user_table.add_row(
            str(user.id),
            user.name,
            user.email,
            user.role,
            user.password
        )

    c.print(user_table)


def table_not_found(table):
    Console().print(
        f"[blue] Table '[bold red]{table}[/bold red]' not found[/blue]")


def user_not_found(id):
    Console().print(
        f"[blue] User with ID '[bold red]{id}[/bold red]' is '[bold red]not found[/bold red]'.")


def param_required():
    Console().print(
        "[blue] '[bold red]Name[/bold red]'[blue], '[bold red]Email[/bold red]'[blue], and "
        "'[bold red]role[/bold red]'[blue] are required for user creation")


def created_succes(user):
    Console().print(
        f"[bold green] '[bold blue]{user.name.upper()}[/bold blue]'created successfully.")


def deleted_success(id, user):
    Console().print(
        f"[blue] User with ID '[bold red]{id}[/bold red]', '[bold red]{user.name.upper()}[/bold red]' "
        "has been '[bold red]deleted[/bold red]'.")


def invalid_pass():
    Console().print(
        "[blue]Password must have at least:\n"
        "[bold red]'one capital'[/bold red] from '[bold red](A-Z)'[/bold red]\n"
        "[bold red]'one lower'[/bold red] from '[bold red](a-z)'[/bold red]\n"
        "[bold red]'one number'[/bold red] from '[bold red](0-9)'[/bold red]\n"
        "[bold red]'one special char'[/bold red] from '[bold red](#?!@$%^&*-)'[/bold red]\n"
        "and at least [bold red]'8 characters'[/bold red]."
    )


def invalid_email():
    Console().print(
        "[blue]The '[bold red]Email[/bold red]' you provided is '[bold red]invalid[/bold red]'")


def invalid_role():
    Console().print(
        "'[bold red]Invalid[/bold red]'[blue] role must be ==> '[bold red]support[/bold red]' or "
        "'[bold red] commercial[/bold red]' or '[bold red]management[/bold red]'.")


def modification_done(user):
    Console().print(
        f"[bold green] '[bold blue]{user.name.upper()}[/bold blue]' successfully modified.")
