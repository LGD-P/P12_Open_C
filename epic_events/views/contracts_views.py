from rich.console import Console
from rich.table import Table
from rich.text import Text


def contracts_table(contracts):
    c = Console()

    contracts_table = Table(show_header=True, header_style="bold blue",
                            title='[bold red]Table: CONTRACTS[/bold red]')
    contracts_table.add_column(
        Text("ID", style="bleu", justify="center", no_wrap=True),
        justify="center", style="yellow",
    )
    contracts_table.add_column(
        Text("UUID", style="blue", justify="center", no_wrap=True),
        justify="center", style="green"
    )
    contracts_table.add_column(
        Text("Client ID", style="blue", justify="center", no_wrap=True),
        justify="center", style="green"
    )
    contracts_table.add_column(
        Text("Management Contact ID", style="blue", justify="center",
             no_wrap=True), justify="center", style="green"
    )
    contracts_table.add_column(
        Text("Total Amount", style="blue", justify="center", no_wrap=True),
        justify="center", style="green"
    )
    contracts_table.add_column(
        Text("Remaining Amount", style="blue", justify="center", no_wrap=True),
        justify="center", style="green"
    )
    contracts_table.add_column(
        Text("Creation Date", style="blue", justify="center", no_wrap=True),
        justify="center", style="red"
    )

    contracts_table.add_column(
        Text("Status", style="blue", justify="center", no_wrap=True),
        justify="center", style="yellow"
    )

    for contract in contracts:
        creation_date = contract.creation_date.strftime('%Y-%m-%d - %H:%M')
        commercial_contact_id = "❌" if contract.management_contact_id is None \
            else contract.management_contact_id
        status = "❌" if contract.status is False else "✅"

        contracts_table.add_row(
            str(contract.id),
            str(contract.uuid),
            str(contract.client_id),
            str(commercial_contact_id),
            str(contract.total_amount),
            str(contract.remaining_amount),
            creation_date,
            status, end_section=True
        )

    print("\n")
    c.print(contracts_table, justify="center")


def table_not_found(table):
    Console().print(
        f"\n[blue] Table '[bold red]{table}[/bold red]' not found[/blue]\n")


def created_succes(contract):
    Console().print(
        f"\n[bold green] ID N° '[bold blue]N°{str(contract.id)}[/bold blue]' "
        f"Contract '[bold blue]N°{str(contract.uuid)}[/bold blue]'created "
        "successfully.\n")


def deleted_success(id, contract):
    Console().print(
        f"\n[blue] Client with ID '[bold red]{id}[/bold red]', UUID "
        "'[bold red]N°{str(contract.uuid)}[/bold red]' "
        "has been '[bold red]deleted[/bold red]'.\n")


def contract_not_found(id):
    Console().print(
        f"\n[blue] Contract with ID '[bold red]{id}[/bold red]' is "
        "'[bold red]not found[/bold red]'.\n")


def modification_done(contract):
    Console().print(
        f"\n[bold green] Contract '[bold blue]N°{str(contract.uuid)}"
        "[/bold blue]' successfully modified.\n")
