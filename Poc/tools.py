import subprocess
import json
from pathlib import Path
from datetime import datetime
from rich.console import Console
from pydantic import BaseModel, Field
import sys

console = Console()


class TOOLS:

    directory = Path("reports")
    directory.mkdir(exist_ok=True)
    max_history = 5

    def __init__(self):

        """
        Initialize the object by loading shell-command configuration and
        setting console color codes.
        """
        
        with open("analysis.json", "r") as file:
            collection = json.load(file)

        self.shell_commands = collection
        self.blue = "\033[34m"
        self.reset = "\033[0m"

    def _subprocess(self, shell: str) -> str:

        """
        Execute a shell command using Popen while streaming live output.

        Args:
            shell (str): Full shell command to execute.

        Returns:
            str: Combined stdout output from the executed command.

        Raises:
            subprocess.CalledProcessError:
                Raised when the command exits with a non-zero return code.
                The exception includes the full captured output.
        """

        console.print("\n[bold blue]Terminal[/bold blue]\n")
        process = subprocess.Popen(
                shell, 
                stdin = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT,
                text = True,
                bufsize = 1,
                shell=True, 
        )

        system = ""
        for line in process.stdout:
            system+=line
            sys.stdout.write(f"{self.blue}{line}{self.reset}")
            sys.stdout.flush()
         
        process.wait()

        if process.returncode !=0:
            raise subprocess.CalledProcessError(
                returncode=process.returncode,
                output=system
        )
        
        return system


    def NMAP(self, url: str = None, level: int = 5) -> str | dict:

        """
            Executes an Nmap scan on a specified target.

            Args:
                url (str): The target URL or IP address to scan. Prompt the user to provide this.
                level (int): The scan intensity or verbosity (default 5). Lower level produce more detailed output, Optionally ask the user to provide a level.

            Returns:
                subprocess.CompletedProcess: On success, contains stdout, stderr, and return code.
                dict: If the scan fails, returns {"error": <description>}.
        """

        try:
            if url is None:
                return None
          
            shell = self.shell_commands["nmap"].format( target = url, level = level)
            result = self._subprocess(shell)
            return result

            
        except Exception as e:
            return {"error": str(e)}


    def W_WEB(self, url: str = None, level: int = 1):

        """
        Performs a WhatWeb scan to identify technologies used on a website.

        Args:
            url (str): The target website URL to analyze. Prompt the user to provide this.
            level (int): The scan verbosity/intensity (default 1). Higher levels detect more details about server software, frameworks, CMS, and plugins.

        Returns:
            subprocess.CompletedProcess: Contains the raw output of the WhatWeb scan, including detected web technologies.
            dict: If the scan fails, returns {"error": <description>}.
        """

        try:
            if url is None:
                return None
    
            shell = self.shell_commands["what_web"].format( target = url, level = level)
            result = subprocess.run(shell, shell=True, text = True, check=True, stdout=subprocess.PIPE)
            return result.stdout
        
        except Exception as e:
             return {"error": str(e)}

    def CURL(self, url: str):
        pass 


    def WSV_NIKTO(self, url: str = None):

        """
        Performs a Nikto web server vulnerability scan on the specified URL.

        Args:
            url (str): The target website URL to scan. Prompt the user to provide this.

        Returns:
            subprocess.CompletedProcess: Contains the raw output of the Nikto scan, including detected vulnerabilities, misconfigurations, and outdated components.
            dict: If the scan fails, returns {"error": <description>}.
        """

        try:
            if url is None:
                return None 
          
            shell = self.shell_commands["nikto"].format( target = url)
            result = subprocess.run(shell, shell=True, text = True, check=True, stdout=subprocess.PIPE)
            return result.stdout
        
        except Exception as e:
             return {"error": str(e)}


    def OPENVS(self, url: str):
        pass 


    def SSL_SCAN(self, url: str, port: str = None):

        """
        Run SSL/TLS scanning commands for a target across predefined ports.

        Args:
            url (str): Target hostname or IP address to scan.
            port (str, optional): Unused parameter; ports are taken from
                                self.shell_commands["sslscan"]["ports"].

        Returns:
            str: Combined scanner output across all configured ports.
            dict: {"error": <message>} if any subprocess or configuration error occurs.
        """

        try:
            if url is None:
                return None 
            
            knowledge_base = ""
        
            for port in self.shell_commands["sslscan"]["ports"]:
                shell = self.shell_commands["sslscan"]['command'].format( target = url, port = port)
                result = subprocess.run(shell, shell=True, text = True, check=True, stdout=subprocess.PIPE)
                knowledge_base+=result.stdout+"\n"
            return knowledge_base
            
        except Exception as e:
            return {"error": str(e)}

    

    def CCV(self, config_path: str = "."):

        """
        Run the configured Trivy command against the given path.

        Args:
            config_path (str): Target directory or file to scan.
    
        Returns:
            str: Standard output from the Trivy scan when successful.
            dict: {"error": <message>} when the scan or subprocess execution fails.
        """

        try:
            if config_path is None:
                return None 
            
    
            shell = self.shell_commands["trivy"].format( path = config_path)
            result = subprocess.run(shell, shell=True, text = True, check=True, stdout=subprocess.PIPE)

            return result.stdout
            
        except Exception as e:
             return {"error": str(e)}

    
    
    
    @classmethod
    def REPORT(cls, content: str) -> str:

        """
        Create a report file.

        Args:
            content (str): Text content to write into the generated report file.

        Returns:
            str: report file creation status.
        """

        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
            file_path = cls.directory / f"file_{timestamp}.txt"
            
            with open(file_path, "w") as f:
                f.write(content)
            print(f"Created {file_path.name}")
            
            files = sorted(cls.directory.iterdir(), key=lambda f: f.stat().st_ctime)
            
            while len(files) > cls.max_history:
                oldest_file = files.pop(0)
                print(f"Deleting {oldest_file.name}")
                oldest_file.unlink()

            return {
                "status": "success",
                "path": str(file_path)
            }
        except Exception as e:
            return {"error": str(e)}









