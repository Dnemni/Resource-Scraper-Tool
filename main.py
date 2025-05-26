import asyncio
import os
from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.text import Text
from rich.markdown import Markdown
from dotenv import load_dotenv
from resource_scraper.scraper import ResourceScraper
from resource_scraper.models import ResourceType

# Initialize Rich console for beautiful output
console = Console()

def truncate_text(text: str, length: int) -> str:
    """Truncate text and add ellipsis if needed"""
    if len(text) <= length:
        return text
    return text[:length-3] + "..."

def create_resource_table(resources: List[Dict]) -> Table:
    """Create a formatted table of resources"""
    table = Table(
        show_header=True,
        header_style="bold magenta",
        border_style="blue",
        expand=True,
        show_lines=True
    )
    
    table.add_column("Type", style="cyan", width=12)
    table.add_column("Title", style="white", ratio=2)
    table.add_column("Score", justify="right", style="green", width=10)
    table.add_column("URL", style="blue", ratio=3)
    
    for resource in resources:
        # Calculate combined score
        score = (resource.credibility_score + resource.relevance_score) / 2
        score_str = f"{score:.2f}"
        
        # Format title and URL with proper wrapping
        title = truncate_text(resource.title, 60)
        url = truncate_text(resource.url, 70)
        
        table.add_row(
            resource.resource_type.value,
            title,
            score_str,
            url
        )
    
    return table

def create_resource_panel(resource: Dict, index: int) -> Panel:
    """Create a detailed panel for a resource"""
    content = [
        Text(resource.title, style="bold white"),
        "",
        Text(f"Type: {resource.resource_type.value}", style="cyan"),
        "",
        Text("Description:", style="cyan"),
        Text(resource.description),
        "",
        Text(f"Credibility Score: {resource.credibility_score:.2f}", style="green"),
        Text(f"Relevance Score: {resource.relevance_score:.2f}", style="green"),
        "",
        Text("URL:", style="blue"),
        Text(resource.url, style="underline blue")
    ]
    
    return Panel(
        "\n".join(str(line) for line in content),
        title=f"[yellow]Resource #{index}[/yellow]",
        border_style="yellow",
        expand=True
    )

async def main():
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    if not os.getenv("SERPER_API_KEY"):
        console.print(Panel(
            "[red]Error: SERPER_API_KEY not found in environment variables.[/red]\n"
            "Please create a .env file with your Serper API key:\n"
            "SERPER_API_KEY=your_key_here",
            title="Configuration Error",
            border_style="red"
        ))
        return

    # Initialize scraper
    scraper = ResourceScraper()
    
    # Get course input
    console.print("\n[bold cyan]Welcome to the Educational Resource Finder![/bold cyan]")
    course_name = Prompt.ask("\n[bold cyan]Enter the course or topic name[/bold cyan]")
    
    # Optional: Get specific resource types
    resource_types = []
    if Prompt.ask("\n[bold cyan]Do you want to filter by resource type?[/bold cyan] (y/n)").lower() == 'y':
        console.print("\n[bold]Available resource types:[/bold]")
        for type_name in ResourceType:
            if Prompt.ask(f"Include [cyan]{type_name.value}[/cyan]? (y/n)").lower() == 'y':
                resource_types.append(type_name)
    
    # Show progress while searching
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        search_task = progress.add_task("[cyan]Searching for educational resources...", total=100)
        
        try:
            # Search for resources
            resources = await scraper.search_resources(course_name)
            progress.update(search_task, completed=100)
            
            # Filter by resource type if specified
            if resource_types:
                resources = [r for r in resources if r.resource_type in resource_types]
            
            # Display results
            if resources:
                console.print("\n[bold green]🎯 Top Educational Resources Found:[/bold green]")
                console.print(f"[green]Found {len(resources)} resources for [bold]{course_name}[/bold][/green]\n")
                
                table = create_resource_table(resources)
                console.print(table)
                
                # Display detailed information for top resources
                console.print("\n[bold yellow]📚 Detailed Information for Top Resources:[/bold yellow]\n")
                for i, resource in enumerate(resources[:5], 1):
                    console.print(create_resource_panel(resource, i))
                    if i < 5:
                        console.print()  # Add spacing between panels
                
                # Add helpful tip
                console.print("\n[dim]💡 Tip: Resources are ranked by credibility and relevance scores[/dim]")
            else:
                console.print("\n[bold red]❌ No resources found.[/bold red]")
                
        except Exception as e:
            console.print(f"\n[bold red]Error occurred while searching:[/bold red] {str(e)}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 