from rich.console import Console
from rich.table import Table
from rich.text import Text


def roles_table(roles):
    c = Console()

    roles_table = Table(show_header=True, header_style="bold blue",
                        title='[bold red]Table: ROLES[/bold red]')
    roles_table.add_column(
        Text("ID", style="bleu", justify="center", no_wrap=True),
        justify="center", style="yellow")
    roles_table.add_column(
        Text("role_name", style="blue", justify="center", no_wrap=True),
        justify="center", style="green")
    roles_table.add_column(
        Text("Backlink to User", style="blue", justify="center", no_wrap=True),
        justify="left", style="green")

    for role in roles:
        for _ in role.users:
            user = "\n".join([f"[bold blue] User ID : "
                              f"[bold yellow]{user.id}[/bold yellow] - Name : "
                              f"[bold green]{user.name}[/bold green]" for user
                              in role.users])

        roles_table.add_row(
            str(role.id),
            role.name.upper(),
            user, end_section=True
        )
    print("\n")
    c.print(roles_table, justify="center")


def created_succes(role):
    Console().print(
        f"[bold green] '[bold blue]{role.name.upper()}[/bold blue]'created "
        "successfully.")


def deleted_success(id, role):
    Console().print(
        f"[blue] Role with ID '[bold red]{id}[/bold red]', '[bold red]"
        f"{role.name.upper()}[/bold red]' "
        "has been '[bold red]deleted[/bold red]'.")


def role_not_found(id):
    Console().print(
        f"[blue] role with ID '[bold red]{id}[/bold red]' is "
        "'[bold red]not found[/bold red]'.")


def id_not_found(id):
    Console().print(
        f"[blue] the User ID '[bold red]{id}[/bold red]' is "
        "'[bold red]not found[/bold red]'.")


def modification_done(role):
    Console().print(
        f"[bold green] '[bold blue]{role.name.upper()}[/bold blue]' "
        "successfully modified.")
