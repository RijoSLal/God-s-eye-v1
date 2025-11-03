from tree_sitter_language_pack import get_language
from tree_sitter import Parser
import subprocess
import typer
from rich.console import Console
from rich.panel import Panel

console = Console()


class Tree_sitter:
    def __init__(self):
        pass 

class Visualization:
    def __init__(self):
        self.max_level = 4

    def tree(self, file_path: str, level: int = 1) -> None:
        """
        create a beautiful visualization of the file hierarchy

        Args:
            file_path (str): path to the current directory
            level (int): maximum depth to display

        Returns:
            None

        Raises:
            ValueError: if the specified depth (level) is greater than 4
            FileNotFoundError: if the 'tree' command-line utility is not installed
            subprocess.CalledProcessError: if an error occurs while running the subprocess
        """
        try: 
            if level > self.max_level: raise ValueError(f"Can’t go deeper than level {self.max_level}, sorry!")

            result = subprocess.run(["tree", "-L", str(level), file_path], capture_output=True, text=True, check=True)
            console.log(
                Panel.fit(
                    result.stdout.strip() or "[dim]No output[/dim]",
                    title=f"[bold green]Filesystem Hierarchy[/bold green] ({file_path})",
                    border_style="blue",
                    subtitle=f"[bold blue]Level {level}[bold blue]",
                )
            )
        except FileNotFoundError:
            console.log("[bold red]Oops:[/bold red] The `tree` command is not installed.")
        except ValueError as e:
            console.log(f"[bold yellow]Warning:[/bold yellow] {e}")
        except subprocess.CalledProcessError as e:
            console.log(f"[bold red]Oops:[/bold red] running tree: {e.stderr}")

    def git_tree(self, file_path): 
        try:
           
            result = subprocess.run(["git", "log", "--all", "--decorate", "--oneline", "--graph", file_path], capture_output=True, text=True, check=True)
            console.log(
                Panel.fit(
                    result.stdout.strip() or "[dim]No output[/dim]",
                    title=f"[bold green]Git Hierarchy[/bold green] ({file_path})",
                    border_style="blue",
                 
                )
            )
        except subprocess.CalledProcessError as e:
            console.log(f"[bold red]Oops:[/bold red] running tree: {e.stderr}")

        

class Seacurity_Quality_Code:
      pass 


class Report:
    pass 


val = Visualization()
val.git_tree(".")
