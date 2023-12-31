from rich.console import Console
from rich.table import Table
from rich.text import Text


def events_table(events):
    c = Console()

    events_table = Table(show_header=True,
                         header_style="bold blue",
                         title='[bold red]Table: EVENTS[/bold red]')
    events_table.add_column(
        Text("ID", style="bleu", justify="center", no_wrap=True),
        justify="center",
        style="yellow",
    )
    events_table.add_column(Text("Name",
                                 style="blue",
                                 justify="center",
                                 no_wrap=True),
                            justify="center",
                            style="green")
    events_table.add_column(Text("Contract ID",
                                 style="blue",
                                 justify="center",
                                 no_wrap=True),
                            justify="center",
                            style="green")
    events_table.add_column(Text("Support Contact ID",
                                 style="blue",
                                 justify="center",
                                 no_wrap=True),
                            justify="center",
                            style="green")
    events_table.add_column(Text("Start date",
                                 style="blue",
                                 justify="center",
                                 no_wrap=True),
                            justify="center",
                            style="red")
    events_table.add_column(Text("End date",
                                 style="blue",
                                 justify="center",
                                 no_wrap=True),
                            justify="center",
                            style="green")
    events_table.add_column(Text("Location",
                                 style="blue",
                                 justify="center",
                                 no_wrap=True),
                            justify="center",
                            style="green")

    events_table.add_column(Text("Attendees",
                                 style="blue",
                                 justify="center",
                                 no_wrap=True),
                            justify="center",
                            style="red")

    events_table.add_column(Text("Notes",
                                 style="blue",
                                 justify="center",
                                 no_wrap=True),
                            justify="center",
                            style="green")

    for event in events:
        start_date = event.start_date.strftime('%d-%m-%Y - %H:%M')
        end_date = event.end_date.strftime('%d-%m-%Y - %H:%M')

        events_table.add_row(str(event.id),
                             event.name,
                             str(event.contract_id),
                             str(event.support_contact_id),
                             start_date,
                             end_date,
                             event.location,
                             str(event.attendees),
                             event.notes,
                             end_section=True)
    print("\n")
    c.print(events_table, justify="center")


def table_not_found(table):
    Console().print(
        f"\n[blue] Table '[bold red]{table}[/bold red]' not found[/blue]\n")


def date_param():
    Console().print(
        "\n[blue] '[bold red]Date[/bold red]'[blue], must be written like this"
        " ==> '[bold red]YYYY-MM-DD - HH:MM[/bold red]'\n")


def end_date_error():
    return Console().print("\n[blue] Unfortunatly you can't go back in time '[bold red]Ending Date[/bold red]' must be"
                           " after '[bold red]Starting Date[/bold red]'\n")


def created_succes(event):
    Console().print(
        f"\n[bold green] ID N° '[bold blue]N°{str(event.id)}[/bold blue]' "
        f"Event '[bold blue]{event.name}[/bold blue]'created successfully.\n")


def deleted_success(id, event):
    Console().print(f"\n[blue] Event with ID '[bold red]{id}[/bold red]', "
                    f"'[bold red]{event.name}[/bold red]' "
                    "has been '[bold red]deleted[/bold red]'.\n")


def event_not_found(id):
    Console().print(f"\n[blue] Event with ID '[bold red]{id}[/bold red]' is "
                    "'[bold red]not found[/bold red]'.\n")


def not_in_charge_of_this_event(id):
    Console().print(f"\n[blue] You are not in charge of the Event with ID '[bold red]{id}[/bold red]' "
                    "'[bold red]contact support team in charge to apply modifications[/bold red]'.\n")


def modification_done(event):
    Console().print(
        f"\n[bold green] Event '[bold blue]{event.name}[/bold blue]' "
        "successfully modified.\n")
