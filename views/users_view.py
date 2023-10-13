from rich.console import Console
from rich.table import Table
from rich.text import Text


def users_table(users, table):
    c = Console()

    user_table = Table(show_header=True, header_style="bold blue",
                       title=f'[bold red]Table: {table}[/bold red]')
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
        "[blue] '[bold red]Name[/bold red]'[blue], '[bold red]Email[/bold red]'[blue], and '[bold red]role[/bold red]'[blue] are required for user creation")


def created_succes():
    Console().print(
        "[bold green] User created successfully.[bold green]")


def deleted_success(id):
    Console().print(
        f"[blue] User with ID '[bold red]{id}[/bold red]' has been '[bold red]deleted[/bold red]'.")
