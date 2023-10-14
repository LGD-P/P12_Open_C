from rich.console import Console
from rich.table import Table
from rich.text import Text
import re
import click


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


    
def pass_is_valid(ctx, param, value):
    regex = re.compile(
        "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
    if value != ctx.params.get('password', None) and re.fullmatch(regex, value) is None:
        Console().print(
    "[blue]Password must have at least:\n"
    "[bold red]'one capital'[/bold red] from '[bold red](A-Z)'[/bold red]\n"
    "[bold red]'one lower'[/bold red] from '[bold red](a-z)'[/bold red]\n"
    "[bold red]'one number'[/bold red] from '[bold red](0-9)'[/bold red]\n"
    "[bold red]'one special char'[/bold red] from '[bold red](#?!@$%^&*-)'[/bold red]\n"
    "and at least [bold red]'8 characters'[/bold red]."
)
        raise click.UsageError(
            "Invalid password. Passwords do not match or not strong enough.")
    return value


def email_is_valid(ctx, param, value):
    regex = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9-]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, value):
        return value
    else:
        Console().print("[blue]The '[bold red]Email[/bold red]' you provided is '[bold red]invalid[/bold red]'")
        raise click.UsageError("Invalid email.")
    
    

def role_is_valid(ctx, param, value):
 
    if value in ["support", "commercial" ,"management"]:
        return value
    else:
        Console().print(
        "'[bold red]Invalid[/bold red]'[blue] role must be ==> '[bold red]support[/bold red]' or '[bold red] commercial[/bold red]' or '[bold red]management[/bold red]'.")
        raise click.UsageError("Invalid role")
        
        
