import logging
import pygame
import os
import time
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.layout import Layout
from rich import print as rprint
from rich.markdown import Markdown
from components.record_audio import record_audio
from components.transcription import transcribe_and_save
from components.listen_for_wakeword import listen_for_wakeword
from components.chat_interface import main as chat_interface_main, play_audio

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Rich console
console = Console()

# Initialize pygame mixer once
pygame.mixer.init()

def create_layout() -> Layout:
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="side", ratio=1),
        Layout(name="body", ratio=2)
    )
    return layout

def wait_for_file(file_path, timeout=10):
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    with progress:
        task = progress.add_task("[cyan]Waiting for file...", total=timeout)
        start_time = time.time()
        while time.time() - start_time < timeout:
            if os.path.exists(file_path):
                progress.update(task, completed=timeout)
                return True
            progress.update(task, completed=time.time() - start_time)
            time.sleep(0.5)
    return False

def play_audio(audio_file):
    try:
        if not wait_for_file(audio_file):
            console.print(Panel(f"[bold red]Error:[/bold red] Audio file not found after waiting: {audio_file}", 
                                title="Audio Playback Error", expand=False))
            return

        with console.status("[bold green]Playing audio...[/bold green]", spinner="dots"):
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        console.print(Panel(f"[bold green]Successfully played audio file:[/bold green] {audio_file}", 
                            title="Audio Playback Complete", expand=False))
    except Exception as e:
        console.print(Panel(f"[bold red]Error playing audio file:[/bold red] {str(e)}", 
                            title="Audio Playback Error", expand=False))

def display_transcription(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        syntax = Syntax(content, "markdown", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title="Transcription", expand=False))
    except Exception as e:
        console.print(f"[bold red]Error displaying transcription:[/bold red] {str(e)}")

def display_llm_response(response):
    md = Markdown(response)
    console.print(Panel(md, title="LLM Response", expand=False))

def create_summary_table(audio_file, transcription_file, response_file):
    table = Table(title="Session Summary")
    table.add_column("Item", style="cyan")
    table.add_column("File", style="magenta")
    table.add_column("Size", justify="right", style="green")
    table.add_row("Audio", audio_file, f"{os.path.getsize(audio_file) / 1024:.2f} KB")
    table.add_row("Transcription", transcription_file, f"{os.path.getsize(transcription_file) / 1024:.2f} KB")
    table.add_row("Response", response_file, f"{os.path.getsize(response_file) / 1024:.2f} KB")
    return table

def main():
    layout = create_layout()
    layout["header"].update(Panel("Voice Assistant", style="bold blue"))
    layout["footer"].update(Panel("Session in progress...", style="bold yellow"))

    console.print(layout)

    # Listen for wake word
    with console.status("[bold yellow]Listening for wake word...[/bold yellow]", spinner="dots") as status:
        listen_for_wakeword()
    layout["side"].update(Panel("[bold green]Wake word detected![/bold green]", expand=False))
    console.print(layout)

    # Record audio
    with console.status("[bold yellow]Recording audio...[/bold yellow]", spinner="dots") as status:
        audio_file = record_audio()
    layout["side"].update(Panel("[bold green]Recording complete[/bold green]", expand=False))
    console.print(layout)

    # Transcribe audio
    with console.status("[bold yellow]Transcribing audio...[/bold yellow]", spinner="dots") as status:
        transcription_file = transcribe_and_save(audio_file)
    layout["side"].update(Panel("[bold green]Transcription complete[/bold green]", expand=False))
    console.print(layout)

    # Display transcription
    display_transcription(transcription_file)

    # Process transcription and generate response
    with console.status("[bold yellow]Generating LLM response...[/bold yellow]", spinner="dots") as status:
        response_audio_file, response_text = chat_interface_main(transcription_file)
    layout["side"].update(Panel("[bold green]LLM response complete[/bold green]", expand=False))
    console.print(layout)

    # Display LLM response
    display_llm_response(response_text)

    # Play the response audio if it was generated successfully
    play_audio(response_audio_file)

    # Create and display summary table
    summary_table = create_summary_table(audio_file, transcription_file, response_audio_file)
    layout["body"].update(summary_table)
    console.print(layout)

    layout["footer"].update(Panel("[bold green]Session Complete[/bold green]", style="bold blue"))
    console.print(layout)

# Quit pygame mixer when the program ends
pygame.mixer.quit()

if __name__ == "__main__":
    main()