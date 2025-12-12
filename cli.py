from rich.console import Console
from rich.table import Table
import typer
import agent
from pyfiglet import Figlet
import sys
import cli_extension
from rich import box
import json

console = Console()

app = typer.Typer(
        add_completion = False, 
        no_args_is_help=True,
        add_help_option=False, 
        rich_markup_mode = "rich"
    )

PANEL = "System Instructions"

@app.command(help = "`God's Eye` SecOps-LLM", rich_help_panel = PANEL)
def eye():

    """
    Launch the primary SecOps-LLM agent. Initializes configuration,
    performs a connectivity test, and if successful, starts
    the interactive agent loop.
    """

    friday = agent.Friday()

    with console.status("[bold white]Initializing God's Eye…[/bold white]", spinner="dots"):
        status_ok = friday.ping()
        
    if status_ok:
        friday.agent()
    else:
        console.print("`God's Eye` initialization blocked, configuration required")

@app.command(help = "Configuration settings", rich_help_panel = PANEL)
def config_settings(
        url: str = typer.Option(
                ...,
                prompt="\033[1;32mOptional custom API endpoint (usually not required)\033[0m ",
                show_default=True
            ),
        api_key: str = typer.Option(
                ...,
                prompt="\033[1;32mAPI key (OpenAI, Custom, etc.)\033[0m ",
                show_default=True
            ),
        model: str = typer.Option(
                ...,
                prompt="\033[1;32mModel\033[0m ",
                show_default=True
            ),
        temp: float = typer.Option(
                ...,
                prompt="\033[1;32mLLM temperature (0->1, default 0.7)\033[0m ",
                show_default=True
            ), 
        
    ):
    
    """
    Update the configuration file with endpoint, key, model, and temperature.
    Reloads the agent and verifies the new settings.
    """

    try:
        with open("config.json", 'r+') as file:
            config = json.load(file)

            config["api_key"] = api_key
            config["url"] = url
            config["model"] = model
            config["temperature"] = temp
            
            file.seek(0)       
            json.dump(config, file, indent=4) 
            file.truncate()     

        console.print(
            f"\n[bold blue]URL:[/bold blue] {url}\n"
            f"[bold blue]API Key:[/bold blue] {api_key}\n"
            f"[bold blue]Model:[/bold blue] {model}\n"
            f"[bold blue]Temperature:[/bold blue] {temp}\n"
        )
        with console.status("[bold white]Setting Values…[/bold white]", spinner="dots"):
            friday = agent.Friday()

        console.print("Config successfull") if friday.ping() else console.print("Config failed")

    except FileNotFoundError:
        console.print("[bold red]Configuration file error :([/bold red]")
        
    


@app.command(help = "`God’s Eye` SecOps-LLM toolkit", rich_help_panel = PANEL)
def list_tools():

    """
    Display a list of available toolkit commands and their descriptions.
    """
        
    table = Table(title="[bold white]Tool-List[/bold white]",  box=box.SIMPLE, title_justify = "center")

    table.add_column("Operation", style="cyan", no_wrap=True)
    table.add_column("Specification", style="white")

    for command, desc in cli_extension.AVAILABLE_TOOLS.items():
        table.add_row(command, desc)
    console.print(table)




@app.command(help = "MCP access of `God’s Eye` toolkit", rich_help_panel = PANEL)
def mcp_tools():
    """
    future MCP tooling integration.
    """
    pass 


def initial_title():
    
    """
    Render the ASCII title and initial header for CLI startup.
    """

    figlet = Figlet(font="standard")
    friday = figlet.renderText("GOD'S EYE")

    typer.echo(f"{friday}", color = "white")
    console.print(f"[bold white]SecOps-LLM[/bold white]")
   
status = True if len(sys.argv) == 1 else False

if not status:
    console.print(
       f"[dim bold white]\n`God's Eye` SecOps-LLM\n[/ dim bold white]"
    )

if __name__ == "__main__":
    if status:
        initial_title()
    app()


