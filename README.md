# DiagraForm

DiagraForm is a Python tool that generates visual diagrams from Terraform state files, making it easier to understand and visualize your infrastructure as code.

## Features

- Generate infrastructure diagrams from Terraform state files
- Group resources by VPC or resource type
- Filter specific resource types to include
- Exclude specific resource types from the diagram
- Create nested clusters for related resources
- Intelligent detection of subnet types (public/private)

## Installation

```bash
# Clone the repository
git clone https://github.com/jeasoft/diagraform.git
cd diagraform

# Install in development mode
pip install -e .
```

## Requirements
- Python 3.9+
- Graphviz (required for the diagrams library)
- Terraform (to generate state files)
## Usage
### Basic Usage
```
# Generate a basic diagram
diagraform generate /path/to/terraform.tfstate
```
### Filtering Resources
You can filter to include only specific resource types:

```
# Include only VPCs and subnets
diagraform generate /path/to/terraform.tfstate 
--filter aws_vpc --filter aws_subnet
```
### Excluding Resources
You can exclude specific resource types from your diagram:

```
# Exclude IAM roles and policies
diagraform generate /path/to/terraform.tfstate 
--exclude aws_iam_role --exclude aws_iam_policy

# Exclude CloudWatch logs
diagraform generate /path/to/terraform.tfstate --exclude aws_cloudwatch_log_group
```
### Grouping Resources
You can group resources by VPC or by resource type:

```
# Group by VPC
diagraform generate /path/to/terraform.tfstate --group-by vpc

# Group by resource type
diagraform generate /path/to/terraform.tfstate --group-by type
```
### Nested Clusters
Create nested clusters for related resources (especially useful for ECS, EKS, and RDS clusters):

```
# Create nested clusters grouped by VPC
diagraform generate /path/to/terraform.tfstate --group-by vpc --nested

# Create nested clusters grouped by resource 
type
diagraform generate /path/to/terraform.tfstate --group-by type --nested
```
### Combining Options
You can combine multiple options for more specific diagrams:

```
# Group by VPC, create nested clusters, and 
exclude IAM resources
diagraform generate /path/to/terraform.tfstate --group-by vpc --nested --exclude aws_iam_role --exclude aws_iam_policy

# Filter to include only specific resources 
and exclude others
diagraform generate /path/to/terraform.tfstate --filter aws_vpc --filter aws_subnet --filter aws_instance --exclude aws_cloudwatch_log_group
```

### Analyzing State Files
You can analyze a state file without generating a diagram:

```
diagraform analyze /path/to/terraform.tfstate
```
## Command Line Options

| Option | Description |
|--------|-------------|
| `state_file` | Path to the Terraform state file (required) |
| `--output`, `-o` | Output directory for the diagram (default: ./diagrams) |
| `--filename`, `-f` | Name of the output file without extension (default: terraform_diagram) |
| `--show/--no-show` | Open the diagram after generation (default: --show) |
| `--filter`, `-t` | Filter to include only specific resource types (can be used multiple times) |
| `--exclude`, `-e` | Exclude specific resource types (can be used multiple times) |
| `--group-by`, `-g` | Group resources by 'vpc', 'type', or 'none' (default: none) |
| `--nested/--no-nested` | Create nested clusters for related resources (default: --no-nested) |
        Too many current requests. Your queue position is 1. Please wait for a while or switch to other models for a smoother experience.

## Examples
### Basic Diagram
```
diagraform generate /path/to/terraform.tfstate
```
### Excluding IAM Resources
```
diagraform generate /path/to/terraform.tfstate --exclude aws_iam_role --exclude aws_iam_policy
```
### Nested VPC Grouping
```
diagraform generate /path/to/terraform.tfstate --group-by vpc --nested
```
## Warning
**I used a AI tool for help me in this project.**
For now just work with AWS resources.
This tool is still in development. Use at your own risk.

## License
MIT

