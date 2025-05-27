"""
Module for analyzing Terraform state files
"""
import json
from typing import Dict, List, Any, Set, Tuple


class TerraformStateParser:
    """Terraform state file analyzer"""

    def __init__(self, state_file_path: str):
        """
        Initializes the parser with the path to the state file
        
        Args:
            state_file_path: Path to the Terraform state file
        """
        self.state_file_path = state_file_path
        self.state_data = None
        self.resources = []
        self.dependencies = {}
        
    def parse(self) -> Tuple[List[Dict[str, Any]], Dict[str, List[str]]]:
        """
        Analyzes the state file and extracts resources and dependencies
        
        Returns:
            Tuple with the list of resources and dictionary of dependencies
        """
        with open(self.state_file_path, 'r') as f:
            self.state_data = json.load(f)
            
        # Extract resources from the root module
        if 'values' in self.state_data and 'root_module' in self.state_data['values']:
            root_resources = self.state_data['values']['root_module'].get('resources', [])
            self.resources.extend(root_resources)
            
            # Extract resources from nested modules if they exist
            if 'child_modules' in self.state_data['values']['root_module']:
                for module in self.state_data['values']['root_module']['child_modules']:
                    if 'resources' in module:
                        self.resources.extend(module['resources'])
        
        # Extract dependencies
        for resource in self.resources:
            resource_id = resource['address']
            self.dependencies[resource_id] = []
            
            # Check if there are explicit dependencies
            if 'depends_on' in resource:
                self.dependencies[resource_id] = resource['depends_on']
                
        return self.resources, self.dependencies
    
    def get_resource_types(self) -> Set[str]:
        """
        Gets the unique resource types in the state
        
        Returns:
            Set of resource types
        """
        if not self.resources:
            self.parse()
            
        return {resource['type'] for resource in self.resources}
    
    def get_resources_by_type(self, resource_type: str) -> List[Dict[str, Any]]:
        """
        Gets all resources of a specific type
        
        Args:
            resource_type: Resource type to filter
            
        Returns:
            List of resources of the specified type
        """
        if not self.resources:
            self.parse()
            
        return [r for r in self.resources if r['type'] == resource_type]