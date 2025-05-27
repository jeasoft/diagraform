"""
Command-line interface for DiagraForm
"""
import click
import os
from .parser import TerraformStateParser
from .generator import DiagramGenerator


@click.group()
def cli():
    """DiagraForm - Diagram generator from Terraform state files"""
    pass


@cli.command()
@click.argument('state_file', type=click.Path(exists=True))
@click.option('--output', '-o', default='./diagrams', help='Output directory for the diagram')
@click.option('--filename', '-f', default='terraform_diagram', help='Filename (without extension)')
@click.option('--show/--no-show', default=True, help='Open the diagram after generation')
@click.option('--filter', '-t', multiple=True, help='Filter by resource types (can be specified multiple times)')
@click.option('--exclude', '-e', multiple=True, help='Exclude resource types (can be specified multiple times)')
@click.option('--group-by', '-g', type=click.Choice(['vpc', 'type', 'none']), default='none', 
              help='Group resources by VPC, type, or none')
@click.option('--nested/--no-nested', default=False, help='Create nested clusters for related resources')
def generate(state_file, output, filename, show, filter, exclude, group_by, nested):
    """Generates a diagram from a Terraform state file"""
    click.echo(f"Analyzing state file: {state_file}")
    
    parser = TerraformStateParser(state_file)
    resources, dependencies = parser.parse()
    
    click.echo(f"Found {len(resources)} resources and {sum(len(deps) for deps in dependencies.values())} dependencies")
    
    # Convert 'none' to None for grouping
    group_by_value = None if group_by == 'none' else group_by
    
    # Convert tuples to lists or None if empty
    filter_list = list(filter) if filter else None
    exclude_list = list(exclude) if exclude else None
    
    if filter_list:
        click.echo(f"Filtering by resource types: {', '.join(filter_list)}")
    
    if exclude_list:
        click.echo(f"Excluding resource types: {', '.join(exclude_list)}")
    
    if group_by_value:
        click.echo(f"Grouping resources by: {group_by_value}")
    
    if nested:
        click.echo("Creating nested clusters for related resources")
    
    click.echo(f"Generating diagram at: {output}/{filename}.png")
    generator = DiagramGenerator(resources, dependencies)
    generator.generate(output, filename, show, filter_list, group_by_value, exclude_list, nested)
    
    click.echo("Diagram generated successfully!")


@cli.command()
@click.argument('state_file', type=click.Path(exists=True))
def analyze(state_file):
    """Analyzes a Terraform state file and displays statistics"""
    click.echo(f"Analyzing state file: {state_file}")
    
    parser = TerraformStateParser(state_file)
    resources, dependencies = parser.parse()
    
    click.echo(f"Total resources: {len(resources)}")
    
    resource_types = parser.get_resource_types()
    click.echo("\nResource types found:")
    for rt in sorted(resource_types):
        count = len(parser.get_resources_by_type(rt))
        click.echo(f"  - {rt}: {count}")
    
    click.echo(f"\nTotal dependencies: {sum(len(deps) for deps in dependencies.values())}")


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()
