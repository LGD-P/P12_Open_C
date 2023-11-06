from rich.console import Console
from rich.table import Table
from rich.text import Text


def clients_table(clients):
    c = Console()

    clients_table = Table(show_header=True, header_style="bold blue",
                          title='[bold red]Table: CLIENTS[/bold red]')
    clients_table.add_column(
        Text("ID", style="bleu", justify="center", no_wrap=True),
        justify="center", style="yellow",
    )
    clients_table.add_column(
        Text("full_name", style="blue", justify="center", no_wrap=True),
        justify="center", style="green"
    )
    clients_table.add_column(
        Text("Email", style="blue", justify="center", no_wrap=True),
        justify="center", style="green"
    )
    clients_table.add_column(
        Text("Phone", style="blue", justify="center", no_wrap=True),
        justify="center", style="green"
    )
    clients_table.add_column(
        Text("Company Name", style="blue", justify="center", no_wrap=True),
        justify="center", style="green"
    )
    clients_table.add_column(
        Text("Creation date", style="blue", justify="center", no_wrap=True),
        justify="center", style="green"
    )
    clients_table.add_column(
        Text("Last Contact", style="blue", justify="center", no_wrap=True),
        justify="center", style="red"
    )

    clients_table.add_column(
        Text("Commercial Contact ID", style="blue", justify="center",
             no_wrap=True), justify="center", style="yellow"
    )

    for client in clients:
        creation_date = client.creation_date.strftime('%d-%m-%Y - %H:%M')
        last_contact_date = client.last_contact_date.strftime(
            '%d-%m-%Y - %H:%M')
        commercial_contact_id = "❌" if client.commercial_contact_id is None \
            else client.commercial_contact_id
        company_name = "❌" if client.company_name is None or \
            client.company_name == 'None' else client.company_name

        clients_table.add_row(
            str(client.id),
            client.full_name,
            client.email,
            client.phone,
            company_name,
            creation_date,
            last_contact_date,
            commercial_contact_id, end_section=True
        )

    print("\n")
    c.print(clients_table, justify="center")


def created_succes(client):
    Console().print(
        f"\n[bold green] '[bold blue]{client.full_name.upper()}"
        "[/bold blue]'created successfully.\n")


def deleted_success(id, client):
    Console().print(
        f"\n[blue] Client with ID '[bold red]{id}[/bold red]', "
        f"'[bold red]{client.full_name.upper()}[/bold red]' "
        "has been '[bold red]deleted[/bold red]'.\n")


def client_not_found(id):
    Console().print(
        f"\n[blue] Client with ID '[bold red]{id}[/bold red]' is "
        "'[bold red]not found[/bold red]'.\n")


def modification_done(client):
    Console().print(
        f"\n[bold green] '[bold blue]{client.full_name.upper()}"
        "[/bold blue]' successfully modified.\n")
