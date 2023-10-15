from rich.console import Console
from rich.table import Table
from rich.text import Text

"""
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    support_contact_id = Column(Integer, ForeignKey('users.id'))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(250), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String(800))
"""


def events_table(events, table):
    c = Console()

    events_table = Table(show_header=True, header_style="bold blue",
                         title=f'[bold red]Table: {table.upper()}[/bold red]')
    events_table.add_column(
        Text("ID", style="bleu", justify="center", no_wrap=True), justify="center", style="yellow",
    )
    events_table.add_column(
        Text("Name", style="blue", justify="center", no_wrap=True), justify="center", style="green"
    )
    events_table.add_column(
        Text("Contract ID", style="blue", justify="center", no_wrap=True), justify="center", style="green"
    )
    events_table.add_column(
        Text("Support Contact ID", style="blue", justify="center", no_wrap=True), justify="center", style="green"
    )
    events_table.add_column(
        Text("Start date", style="blue", justify="center", no_wrap=True), justify="center", style="red"
    )
    events_table.add_column(
        Text("End date", style="blue", justify="center", no_wrap=True), justify="center", style="green"
    )
    events_table.add_column(
        Text("Location", style="blue", justify="center", no_wrap=True), justify="center", style="green"
    )

    events_table.add_column(
        Text("Attendees", style="blue", justify="center", no_wrap=True), justify="center", style="red"
    )

    events_table.add_column(
        Text("Notes", style="blue", justify="center", no_wrap=True), justify="center", style="green"
    )

    for event in events:
        start_date = event.start_date.strftime('%Y-%m-%d - %H:%M')
        end_date = event.end_date.strftime('%Y-%m-%d - %H:%M')

        events_table.add_row(
            str(event.id),
            event.name,
            str(event.contract_id),
            str(event.support_contact_id),
            start_date,
            end_date,
            event.location,
            str(event.attendees),
            event.notes
        )

    c.print(events_table)


def table_not_found(table):
    Console().print(
        f"[blue] Table '[bold red]{table}[/bold red]' not found[/blue]")


def param_required():
    Console().print(
        "[blue] '[bold red]Name[/bold red]'[blue], '[bold red]Contract Id [/bold red]'[blue], and "
        "'[bold red]Support contact_id[/bold red]', '[bold red]start date[/bold red][blue] "
        "'[bold red]End date[/bold red]', '[bold red]location[/bold red]' and '[bold red]Attendees[/bold red]' "
        "are required for clients creation")


def created_succes(event):
    Console().print(
        f"[bold green] ID N° '[bold blue]N°{str(event.id)}[/bold blue]' "
        f"Event '[bold blue]{event.name}[/bold blue]'created successfully.")


def deleted_success(id, event):
    Console().print(
        f"[blue] Event with ID '[bold red]{id}[/bold red]', '[bold blue]{event.name}[/bold blue]' "
        "has been '[bold red]deleted[/bold red]'.")


def event_not_found(id):
    Console().print(
        f"[blue] Event with ID '[bold red]{id}[/bold red]' is '[bold red]not found[/bold red]'.")


def modification_done(event):
    Console().print(
        f"[bold green] Event'[bold blue]{event.name}[/bold blue]' successfully modified.")
