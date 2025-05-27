"""
Module for generating diagrams from Terraform resources
"""
from typing import Dict, List, Any, Optional
from diagrams import Diagram, Cluster
import diagrams.aws.compute
import diagrams.aws.network
import diagrams.aws.storage
import diagrams.aws.database
import diagrams.aws.security
import diagrams.aws.integration
import diagrams.aws.management
import diagrams.aws.analytics
import diagrams.aws.ml
import diagrams.aws.iot
import diagrams.aws.mobile
import diagrams.aws.game
import diagrams.aws.ar
import diagrams.aws.blockchain
import diagrams.aws.business
import diagrams.aws.engagement
import diagrams.aws.media
import diagrams.aws.migration
import diagrams.aws.quantum
import diagrams.aws.satellite
import diagrams.aws.robotics
import diagrams.aws.general

# Specific imports to maintain compatibility with existing code
from diagrams.aws.compute import EC2, AutoScaling, Lambda
from diagrams.aws.network import (
    VPC, InternetGateway, RouteTable, PublicSubnet as Subnet,
    PublicSubnet, PrivateSubnet, NATGateway, TransitGateway,
    ElasticLoadBalancing, ElbApplicationLoadBalancer as ApplicationLoadBalancer,
    NLB as NetworkLoadBalancer, CloudFront, Route53, APIGateway
)
from diagrams.aws.security import ACM, WAF
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS, Aurora, Dynamodb
from diagrams.aws.management import CloudwatchRule as CloudwatchEventRule
from diagrams.aws.general import General
import os
import re


class DiagramGenerator:
    """Diagram generator from Terraform resources"""
    
    # Mapping of AWS resource types to diagrams node classes
    AWS_RESOURCE_MAP = {
        # Compute
        'aws_instance': EC2,
        'aws_autoscaling_group': AutoScaling,
        'aws_lambda_function': Lambda,
        'aws_batch_compute_environment': diagrams.aws.compute.Batch,
        'aws_elastic_beanstalk_application': diagrams.aws.compute.ElasticBeanstalk,
        'aws_eks_cluster': diagrams.aws.compute.EKS,
        'aws_ecs_cluster': diagrams.aws.compute.ECS,
        'aws_ecs_service': diagrams.aws.compute.ECS,
        'aws_ecs_task_definition': diagrams.aws.compute.ElasticContainerServiceService,
        'aws_lightsail_instance': diagrams.aws.compute.Lightsail,
        'aws_outposts': diagrams.aws.compute.Outposts,
        'aws_serverless_application_repository': diagrams.aws.compute.SAR,
        'aws_app_runner_service': diagrams.aws.compute.AppRunner,
        'aws_fargate_task': diagrams.aws.compute.Fargate,
        'aws_ec2_spot': diagrams.aws.compute.EC2SpotInstance,
        'aws_ec2_image_builder': diagrams.aws.compute.EC2ImageBuilder,
        'aws_compute_optimizer': diagrams.aws.compute.ComputeOptimizer,
        'aws_wavelength': diagrams.aws.compute.Wavelength,
        'aws_thinkbox_deadline': diagrams.aws.compute.ThinkboxDeadline,
        'aws_thinkbox_frost': diagrams.aws.compute.ThinkboxFrost,
        'aws_thinkbox_krakatoa': diagrams.aws.compute.ThinkboxKrakatoa,
        'aws_thinkbox_sequoia': diagrams.aws.compute.ThinkboxSequoia,
        'aws_thinkbox_stoke': diagrams.aws.compute.ThinkboxStoke,

        
        # Network
        'aws_vpc': VPC,
        'aws_internet_gateway': InternetGateway,
        'aws_subnet': Subnet,  # Genérico
        'aws_route_table': RouteTable,
        'aws_nat_gateway': NATGateway,
        'aws_transit_gateway': TransitGateway,
        'aws_lb': ElasticLoadBalancing,
        'aws_alb': ApplicationLoadBalancer,
        'aws_nlb': NetworkLoadBalancer,
        'aws_cloudfront_distribution': CloudFront,
        'aws_route53_zone': Route53,
        'aws_api_gateway_rest_api': APIGateway,
        'aws_api_gateway_v2_api': diagrams.aws.network.APIGatewayEndpoint,
        'aws_apigatewayv2_api': diagrams.aws.network.APIGatewayEndpoint,
        'aws_vpc_endpoint': diagrams.aws.network.Endpoint,
        'aws_vpc_peering_connection': diagrams.aws.network.VPCPeering,
        'aws_direct_connect': diagrams.aws.network.DirectConnect,
        'aws_global_accelerator': diagrams.aws.network.GlobalAccelerator,
        'aws_app_mesh': diagrams.aws.network.AppMesh,
        'aws_cloud_map': diagrams.aws.network.CloudMap,
        'aws_service_discovery_service': diagrams.aws.network.CloudMap,
        'aws_elastic_load_balancing': diagrams.aws.network.ElasticLoadBalancing,
        'aws_cloudfront_streamingdistribution': diagrams.aws.network.CloudFrontStreamingDistribution,
        'aws_vpc_flow_logs': diagrams.aws.network.VPCFlowLogs,
        'aws_network_firewall': diagrams.aws.network.NetworkFirewall,
        
        # Storage
        'aws_s3_bucket': S3,
        'aws_efs_file_system': diagrams.aws.storage.EFS,
        'aws_fsx_lustre_file_system': diagrams.aws.storage.FSx,
        'aws_fsx_windows_file_system': diagrams.aws.storage.FSx,
        'aws_fsx_ontap_file_system': diagrams.aws.storage.FSx,
        'aws_storage_gateway': diagrams.aws.storage.StorageGateway,
        'aws_backup_vault': diagrams.aws.storage.Backup,
        'aws_ebs_volume': diagrams.aws.storage.EBS,
        'aws_snowball': diagrams.aws.storage.Snowball,
        'aws_snowball_edge': diagrams.aws.storage.SnowballEdge,
        'aws_snowmobile': diagrams.aws.storage.Snowmobile,
        'aws_s3_glacier': diagrams.aws.storage.S3Glacier,

        
        # Database
        'aws_db_instance': RDS,
        'aws_rds_cluster': Aurora,
        'aws_dynamodb_table': Dynamodb,
        'aws_elasticache_cluster': diagrams.aws.database.ElastiCache,
        'aws_elasticache_replication_group': diagrams.aws.database.ElastiCache,
        'aws_neptune_cluster': diagrams.aws.database.Neptune,
        'aws_redshift_cluster': diagrams.aws.database.Redshift,
        'aws_documentdb_cluster': diagrams.aws.database.DocumentDB,
        'aws_timestream_database': diagrams.aws.database.Timestream,
        'aws_keyspaces_keyspace': diagrams.aws.database.KeyspacesManagedApacheCassandraService,
        'aws_qldb_ledger': diagrams.aws.database.QLDB,
        'aws_database_migration_service': diagrams.aws.database.DatabaseMigrationService,
        'aws_dms_replication_instance': diagrams.aws.database.DatabaseMigrationService,
        'aws_dax_cluster': diagrams.aws.database.DynamodbDax,
        'aws_dms_event_subscription': diagrams.aws.database.Database,
        'aws_memorydb_cluster': diagrams.aws.database.ElasticacheForMemcached,
        
        # Security
        'aws_acm_certificate': ACM,
        'aws_waf_web_acl': WAF,
        'aws_iam_role': diagrams.aws.security.IAM,
        'aws_iam_user': diagrams.aws.security.IAMPermissions,
        'aws_iam_group': diagrams.aws.security.IAMRole,
        'aws_iam_policy': diagrams.aws.security.IAMPermissions,
        'aws_kms_key': diagrams.aws.security.KMS,
        'aws_cognito_user_pool': diagrams.aws.security.Cognito,
        'aws_cognito_identity_pool': diagrams.aws.security.Cognito,
        'aws_secrets_manager_secret': diagrams.aws.security.SecretsManager,
        'aws_inspector_assessment_template': diagrams.aws.security.Inspector,
        'aws_shield_protection': diagrams.aws.security.Shield,
        'aws_security_hub_hub': diagrams.aws.security.SecurityHub,
        'aws_directory_service_directory': diagrams.aws.security.DirectoryService,
        'aws_artifact': diagrams.aws.security.Artifact,
        'aws_certificate_authority': diagrams.aws.security.CertificateManager,
        'aws_detective': diagrams.aws.security.Detective,
        'aws_firewall_manager': diagrams.aws.security.FirewallManager,
        'aws_key_management_service': diagrams.aws.security.KeyManagementService,
        'aws_network_firewall': diagrams.aws.network.NetworkFirewall,
        'aws_resource_access_manager': diagrams.aws.security.ResourceAccessManager,
        'aws_single_sign_on': diagrams.aws.security.SingleSignOn,
        'aws_waf': diagrams.aws.security.WAF,
        'aws_waf_regional': diagrams.aws.security.WAF,
        
        # Integration
        'aws_api_gateway': APIGateway,
        'aws_sns_topic': diagrams.aws.integration.SNS,
        'aws_sqs_queue': diagrams.aws.integration.SQS,
        'aws_cloudwatch_event_rule': CloudwatchEventRule,
        'aws_step_functions_state_machine': diagrams.aws.integration.StepFunctions,
        'aws_mq_broker': diagrams.aws.integration.MQ,
        'aws_application_integration': diagrams.aws.integration.ApplicationIntegration,
        'aws_console_mobile_application': diagrams.aws.integration.ConsoleMobileApplication,
        'aws_cloudwatch_event_bus': diagrams.aws.integration.EventbridgeCustomEventBusResource,
        'aws_express_workflows': diagrams.aws.integration.ExpressWorkflows,
        
        # Management
        'aws_cloudwatch_dashboard': diagrams.aws.management.Cloudwatch,
        'aws_cloudwatch_alarm': diagrams.aws.management.CloudwatchAlarm,
        'aws_cloudwatch_log_group': diagrams.aws.management.CloudwatchLogs,
        'aws_cloudtrail': diagrams.aws.management.Cloudtrail,
        'aws_config': diagrams.aws.management.Config,
        'aws_organizations_organization': diagrams.aws.management.Organizations,
        'aws_auto_scaling': diagrams.aws.management.AutoScaling,
        'aws_systems_manager_parameter': diagrams.aws.management.SystemsManager,
        'aws_ssm_parameter': diagrams.aws.management.SystemsManager,
        'aws_ssm_document': diagrams.aws.management.SystemsManagerDocuments,
        'aws_license_manager': diagrams.aws.management.LicenseManager,
        'aws_service_catalog_portfolio': diagrams.aws.management.ServiceCatalog,
        'aws_trusted_advisor': diagrams.aws.management.TrustedAdvisor,
        'aws_well_architected_tool': diagrams.aws.management.WellArchitectedTool,
        'aws_control_tower': diagrams.aws.management.ControlTower,
        
        # Analytics
        'aws_athena': diagrams.aws.analytics.Athena,
        'aws_emr_cluster': diagrams.aws.analytics.EMR,
        'aws_glue_crawler': diagrams.aws.analytics.Glue,
        'aws_glue_job': diagrams.aws.analytics.GlueCrawlers,
        'aws_glue_catalog': diagrams.aws.analytics.GlueDataCatalog,
        'aws_kinesis_stream': diagrams.aws.analytics.KinesisDataStreams,
        'aws_kinesis_firehose_delivery_stream': diagrams.aws.analytics.KinesisDataFirehose,
        'aws_kinesis_analytics_application': diagrams.aws.analytics.KinesisDataAnalytics,
        'aws_quicksight': diagrams.aws.analytics.Quicksight,
        'aws_data_pipeline': diagrams.aws.analytics.DataPipeline,
        'aws_lake_formation': diagrams.aws.analytics.LakeFormation,
        'aws_elasticsearch_domain': diagrams.aws.analytics.ElasticsearchService,
        'aws_msk_cluster': diagrams.aws.analytics.ManagedStreamingForKafka,

        
        # Machine Learning
        'aws_sagemaker_notebook_instance': diagrams.aws.ml.SagemakerNotebook,
        'aws_sagemaker_model': diagrams.aws.ml.Sagemaker,
        'aws_sagemaker_training_job': diagrams.aws.ml.SagemakerTrainingJob,
        'aws_sagemaker_endpoint': diagrams.aws.ml.SagemakerModel,
        'aws_comprehend': diagrams.aws.ml.Comprehend,
        'aws_rekognition': diagrams.aws.ml.Rekognition,
        'aws_polly': diagrams.aws.ml.Polly,
        'aws_textract': diagrams.aws.ml.Textract,
        'aws_lex': diagrams.aws.ml.Lex,
        'aws_forecast': diagrams.aws.ml.Forecast,
        'aws_personalize': diagrams.aws.ml.Personalize,
        'aws_translate': diagrams.aws.ml.Translate,
        'aws_transcribe': diagrams.aws.ml.Transcribe,
        'aws_deep_learning_containers': diagrams.aws.ml.DeepLearningContainers,
        'aws_elastic_inference': diagrams.aws.ml.ElasticInference,
        'aws_fraud_detector': diagrams.aws.ml.FraudDetector,
        'aws_kendra': diagrams.aws.ml.Kendra,
        
        # IoT
        'aws_iot_core': diagrams.aws.iot.IotCore,
        'aws_iot_analytics': diagrams.aws.iot.IotAnalytics,
        'aws_iot_button': diagrams.aws.iot.IotButton,
        'aws_iot_certificate': diagrams.aws.iot.IotCertificate,
        'aws_iot_device_defender': diagrams.aws.iot.IotDeviceDefender,
        'aws_iot_device_management': diagrams.aws.iot.IotDeviceManagement,
        'aws_iot_events': diagrams.aws.iot.IotEvents,
        'aws_iot_greengrass': diagrams.aws.iot.IotGreengrass,
        'aws_iot_policy': diagrams.aws.iot.IotPolicy,
        'aws_iot_rule': diagrams.aws.iot.IotRule,
        'aws_iot_sitewise': diagrams.aws.iot.IotSitewise,
        'aws_iot_things_graph': diagrams.aws.iot.IotThingsGraph,
        'aws_iot_1click': diagrams.aws.iot.Iot1Click,
        'aws_iot_analytics': diagrams.aws.iot.IotAnalytics,
        'aws_iot_button': diagrams.aws.iot.IotButton,
        
        # Mobile
        'aws_amplify': diagrams.aws.mobile.Amplify,
        'aws_appsync': diagrams.aws.mobile.Appsync,
        'aws_device_farm': diagrams.aws.mobile.DeviceFarm,
        'aws_pinpoint': diagrams.aws.mobile.Pinpoint,
        
        # Blockchain
        'aws_managed_blockchain': diagrams.aws.blockchain.ManagedBlockchain,
        
        # Business Applications
        'aws_alexa_for_business': diagrams.aws.business.AlexaForBusiness,
        'aws_chime': diagrams.aws.business.Chime,
        'aws_workmail': diagrams.aws.business.Workmail,
        
        # Customer Engagement
        'aws_connect': diagrams.aws.engagement.Connect,
        
        # Media Services
        'aws_elastic_transcoder': diagrams.aws.media.ElasticTranscoder,
        'aws_elemental_mediaconnect': diagrams.aws.media.ElementalMediaconnect,
        'aws_elemental_mediaconvert': diagrams.aws.media.ElementalMediaconvert,
        'aws_elemental_medialive': diagrams.aws.media.ElementalMedialive,
        'aws_elemental_mediapackage': diagrams.aws.media.ElementalMediapackage,
        'aws_elemental_mediastore': diagrams.aws.media.ElementalMediastore,
        'aws_elemental_mediatailor': diagrams.aws.media.ElementalMediatailor,
        
        # Migration & Transfer
        'aws_application_discovery_service': diagrams.aws.migration.ApplicationDiscoveryService,
        'aws_cloudendure_migration': diagrams.aws.migration.CloudendureMigration,
        'aws_database_migration_service': diagrams.aws.migration.DatabaseMigrationService,
        'aws_datasync': diagrams.aws.migration.Datasync,
        'aws_migration_hub': diagrams.aws.migration.MigrationHub,
        'aws_server_migration_service': diagrams.aws.migration.ServerMigrationService,
        'aws_snowball': diagrams.aws.migration.Snowball,
        'aws_snowball_edge': diagrams.aws.migration.SnowballEdge,
        'aws_snowmobile': diagrams.aws.migration.Snowmobile,
        
        # Front End Web & Mobile
        'aws_amplify_console': diagrams.aws.mobile.Amplify,
        
        # Quantum Technologies
        'aws_braket': diagrams.aws.quantum.Braket,
        
        # Satellite
        'aws_ground_station': diagrams.aws.satellite.GroundStation,
        
        # Robotics
        'aws_robomaker': diagrams.aws.robotics.Robomaker,
        
        # Containers
        'aws_ecr_repository': diagrams.aws.compute.ECR,
        
        # General
        'aws_marketplace': diagrams.aws.general.Marketplace,
        'aws_general': General,
    }
    
    def __init__(self, resources: List[Dict[str, Any]], dependencies: Dict[str, List[str]]):
        """
        Initializes the generator with resources and dependencies
        
        Args:
            resources: List of resources extracted from the state
            dependencies: Dictionary of resource dependencies
        """
        self.resources = resources
        self.dependencies = dependencies
        self.nodes = {}  # Stores nodes created by address
    
    def _determine_subnet_type(self, resource: Dict[str, Any]) -> Any:
        """
        Determines whether a subnet is public or private based on its attributes
        
        Args:
            resource: Subnet-type resource
            
        Returns:
            Appropriate node class (PublicSubnet, PrivateSubnet, or Subnet)
        """
        name = resource.get('name', '').lower()
        is_public = False
        if 'values' in resource and isinstance(resource['values'], dict):
            if resource['values'].get('map_public_ip_on_launch'):
                is_public = True
            tags = resource['values'].get('tags', {})
            if isinstance(tags, dict):
                subnet_type = tags.get('Type', '').lower()
                if 'public' in subnet_type:
                    is_public = True
                elif 'private' in subnet_type:
                    is_public = False
        if 'public' in name:
            is_public = True
        elif 'private' in name:
            is_public = False
        return PublicSubnet if is_public else PrivateSubnet
    
    def generate(self, output_path: str, filename: str = "terraform_diagram", show: bool = True, 
                 filter_types: List[str] = None, group_by: str = None, exclude_types: List[str] = None,
                 nested_clusters: bool = False):
        """
        Generates the diagram and saves it to the specified path
        
        Args:
            output_path: Directory where the diagram will be saved
            filename: Filename (without extension)
            show: If True, opens the diagram after generation
            filter_types: List of resource types to include (None to include all)
            group_by: Criterion for grouping resources ('vpc', 'type', None for no grouping)
            exclude_types: List of resource types to exclude (e.g., permissions, secrets)
            nested_clusters: If True, creates nested clusters for related resources
        """
        os.makedirs(output_path, exist_ok=True)
        
        with Diagram("Infraestructura Terraform", filename=os.path.join(output_path, filename), show=show):
            # Filter resources if necessary
            filtered_resources = self.resources
            if filter_types:
                filtered_resources = [r for r in self.resources if r['type'] in filter_types]
            
            # Apply inclusion filters
            if filter_types:
                filtered_resources = [r for r in filtered_resources if r['type'] in filter_types]
            
            # Apply exclusion filters
            if exclude_types:
                filtered_resources = [r for r in filtered_resources if r['type'] not in exclude_types]
            
            # Create nodes for each resource according to the grouping type
            if group_by == 'vpc':
                if nested_clusters:
                    self._generate_nested_by_vpc(filtered_resources)
                else:
                    self._generate_grouped_by_vpc(filtered_resources)
            elif group_by == 'type':
                if nested_clusters:
                    self._generate_nested_by_type(filtered_resources)
                else:
                    self._generate_grouped_by_type(filtered_resources)
            else:
                self._generate_flat(filtered_resources)
            
            # Connect nodes based on dependencies
            for resource_id, deps in self.dependencies.items():
                if resource_id in self.nodes:
                    for dep in deps:
                        if dep in self.nodes:
                            self.nodes[dep] >> self.nodes[resource_id]
    
    def _generate_flat(self, resources: List[Dict[str, Any]]):
        """Generates a flat diagram without grouping"""
        for resource in resources:
            address = resource['address']
            resource_type = resource['type']
            name = resource['name']
            
            # Special case for subnets
            if resource_type == 'aws_subnet':
                node_class = self._determine_subnet_type(resource)
            else:
                # Get the corresponding node class or use General as a fallback
                node_class = self.AWS_RESOURCE_MAP.get(resource_type, General)
            
            # Create node
            self.nodes[address] = node_class(f"{name}\n({resource_type})")
    
    def _generate_grouped_by_vpc(self, resources: List[Dict[str, Any]]):
        """Generates a diagram grouped by VPC"""
        # First identify all VPCs
        vpcs = [r for r in resources if r['type'] == 'aws_vpc']
        vpc_nodes = {}
        
        # Create clusters for each VPC
        for vpc in vpcs:
            vpc_address = vpc['address']
            vpc_name = vpc.get('name', 'Unknown VPC')
            
            with Cluster(f"VPC: {vpc_name}"):
                # Create node for VPC
                vpc_node = VPC(f"{vpc_name}\n({vpc['type']})")
                self.nodes[vpc_address] = vpc_node
                vpc_nodes[vpc_address] = vpc_node
                
                # Encontrar recursos que dependen de esta VPC
                vpc_resources = []
                for resource in resources:
                    if resource['type'] != 'aws_vpc':
                        # Verificar si el recurso tiene vpc_id en sus valores
                        if 'values' in resource and isinstance(resource['values'], dict):
                            vpc_id = resource['values'].get('vpc_id')
                            # Buscar la VPC correspondiente
                            for v in vpcs:
                                if 'values' in v and v['values'].get('id') == vpc_id:
                                    if v['address'] == vpc_address:
                                        vpc_resources.append(resource)
                                        break
                
                # Create nodes for the resources in this VPC
                for resource in vpc_resources:
                    address = resource['address']
                    resource_type = resource['type']
                    name = resource['name']
                    
                    # Special case for subnets
                    if resource_type == 'aws_subnet':
                        node_class = self._determine_subnet_type(resource)
                    else:
                        node_class = self.AWS_RESOURCE_MAP.get(resource_type, General)
                    
                    self.nodes[address] = node_class(f"{name}\n({resource_type})")
        
        # Create nodes for resources that do not belong to any VPC
        with Cluster("Global Resources"):
            for resource in resources:
                if resource['address'] not in self.nodes and resource['type'] != 'aws_vpc':
                    address = resource['address']
                    resource_type = resource['type']
                    name = resource['name']
                    
                    node_class = self.AWS_RESOURCE_MAP.get(resource_type, General)
                    self.nodes[address] = node_class(f"{name}\n({resource_type})")
    
    def _generate_grouped_by_type(self, resources: List[Dict[str, Any]]):
        """Generates a diagram grouping resources by type"""
        # grouping resources bt type
        resource_types = {}
        for resource in resources:
            resource_type = resource['type']
            if resource_type not in resource_types:
                resource_types[resource_type] = []
            resource_types[resource_type].append(resource)
        
        # Crear clusters para cada tipo de recurso
        for resource_type, type_resources in resource_types.items():
            # Obtener un nombre más amigable para el tipo
            friendly_name = resource_type.replace('aws_', '').replace('_', ' ').title()
            
            with Cluster(f"{friendly_name}"):
                for resource in type_resources:
                    address = resource['address']
                    name = resource['name']
                    
                    # Caso especial para subnets
                    if resource_type == 'aws_subnet':
                        node_class = self._determine_subnet_type(resource)
                    else:
                        node_class = self.AWS_RESOURCE_MAP.get(resource_type, General)
                    
                    self.nodes[address] = node_class(f"{name}")

    def _generate_nested_by_vpc(self, resources: List[Dict[str, Any]]):
        """Genera un diagrama con clusters anidados agrupados por VPC"""
        # Primero identificar todas las VPCs
        vpcs = [r for r in resources if r['type'] == 'aws_vpc']
        vpc_nodes = {}
        
        # Crear clusters para cada VPC
        for vpc in vpcs:
            vpc_address = vpc['address']
            vpc_name = vpc.get('name', 'Unknown VPC')
            
            with Cluster(f"VPC: {vpc_name}"):
                # Crear nodo para la VPC
                vpc_node = VPC(f"{vpc_name}\n({vpc['type']})")
                self.nodes[vpc_address] = vpc_node
                vpc_nodes[vpc_address] = vpc_node
                
                # Encontrar recursos que dependen de esta VPC
                vpc_resources = []
                for resource in resources:
                    if resource['type'] != 'aws_vpc':
                        # Verificar si el recurso tiene vpc_id en sus valores
                        if 'values' in resource and isinstance(resource['values'], dict):
                            vpc_id = resource['values'].get('vpc_id')
                            # Buscar la VPC correspondiente
                            for v in vpcs:
                                if 'values' in v and v['values'].get('id') == vpc_id:
                                    if v['address'] == vpc_address:
                                        vpc_resources.append(resource)
                                        break
                
                # Agrupar recursos por tipo dentro de la VPC
                resource_by_type = {}
                for resource in vpc_resources:
                    resource_type = resource['type']
                    if resource_type not in resource_by_type:
                        resource_by_type[resource_type] = []
                    resource_by_type[resource_type].append(resource)
                
                # Crear clusters anidados para cada tipo de recurso
                for resource_type, type_resources in resource_by_type.items():
                    # Obtener un nombre más amigable para el tipo
                    friendly_name = resource_type.replace('aws_', '').replace('_', ' ').title()
                    
                    # Crear cluster para el tipo de recurso
                    with Cluster(f"{friendly_name}"):
                        for resource in type_resources:
                            address = resource['address']
                            name = resource['name']
                            
                            # Caso especial para subnets
                            if resource_type == 'aws_subnet':
                                node_class = self._determine_subnet_type(resource)
                            else:
                                node_class = self.AWS_RESOURCE_MAP.get(resource_type, General)
                            
                            self.nodes[address] = node_class(f"{name}")
                            
                            # Crear clusters anidados para recursos que tienen dependencias específicas
                            if resource_type in ['aws_ecs_cluster', 'aws_eks_cluster', 'aws_rds_cluster']:
                                self._create_nested_dependencies(resource, resources)
        
        # Crear nodos para recursos que no pertenecen a ninguna VPC
        with Cluster("Recursos Globales"):
            global_resources = [r for r in resources if r['address'] not in self.nodes and r['type'] != 'aws_vpc']
            
            # Agrupar recursos globales por tipo
            global_by_type = {}
            for resource in global_resources:
                resource_type = resource['type']
                if resource_type not in global_by_type:
                    global_by_type[resource_type] = []
                global_by_type[resource_type].append(resource)
            
            # Crear clusters anidados para cada tipo de recurso global
            for resource_type, type_resources in global_by_type.items():
                friendly_name = resource_type.replace('aws_', '').replace('_', ' ').title()
                
                with Cluster(f"{friendly_name}"):
                    for resource in type_resources:
                        address = resource['address']
                        name = resource['name']
                        
                        node_class = self.AWS_RESOURCE_MAP.get(resource_type, General)
                        self.nodes[address] = node_class(f"{name}")
                        
                        # Crear clusters anidados para recursos que tienen dependencias específicas
                        if resource_type in ['aws_ecs_cluster', 'aws_eks_cluster', 'aws_rds_cluster']:
                            self._create_nested_dependencies(resource, resources)

    def _generate_nested_by_type(self, resources: List[Dict[str, Any]]):
        """Genera un diagrama con clusters anidados agrupados por tipo"""
        # Agrupar recursos por tipo
        resource_types = {}
        for resource in resources:
            resource_type = resource['type']
            if resource_type not in resource_types:
                resource_types[resource_type] = []
            resource_types[resource_type].append(resource)
        
        # Crear clusters para cada tipo de recurso
        for resource_type, type_resources in resource_types.items():
            # Obtener un nombre más amigable para el tipo
            friendly_name = resource_type.replace('aws_', '').replace('_', ' ').title()
            
            with Cluster(f"{friendly_name}"):
                for resource in type_resources:
                    address = resource['address']
                    name = resource['name']
                    
                    # Caso especial para subnets
                    if resource_type == 'aws_subnet':
                        node_class = self._determine_subnet_type(resource)
                    else:
                        node_class = self.AWS_RESOURCE_MAP.get(resource_type, General)
                    
                    self.nodes[address] = node_class(f"{name}")
                    
                    # Crear clusters anidados para recursos que tienen dependencias específicas
                    if resource_type in ['aws_ecs_cluster', 'aws_eks_cluster', 'aws_rds_cluster']:
                        self._create_nested_dependencies(resource, resources)

    def _create_nested_dependencies(self, parent_resource: Dict[str, Any], all_resources: List[Dict[str, Any]], depth: int = 0, max_depth: int = 3, processed_resources: set[str] = None):
        """Crea un cluster anidado para los recursos que dependen del recurso padre de manera recursiva"""
        # Inicializar el conjunto de recursos procesados si es None
        if processed_resources is None:
            processed_resources = set()
            
        # Evitar recursión infinita o demasiado profunda
        if depth >= max_depth:
            return
            
        parent_address = parent_resource['address']
        parent_name = parent_resource['name']
        parent_type = parent_resource['type']
        
        # Evitar procesar el mismo recurso más de una vez
        if parent_address in processed_resources:
            return
            
        processed_resources.add(parent_address)
        
        # Encontrar recursos que dependen de este recurso padre
        dependent_resources = []
        
        # Buscar por ID en los valores
        parent_id = None
        if 'values' in parent_resource and isinstance(parent_resource['values'], dict):
            parent_id = parent_resource['values'].get('id')
        
        if parent_id:
            for resource in all_resources:
                if resource['address'] != parent_address and resource['address'] not in processed_resources:  # Evitar el propio recurso y recursos ya procesados
                    if 'values' in resource and isinstance(resource['values'], dict):
                        # Buscar referencias al ID del padre en los valores
                        for key, value in resource['values'].items():
                            if isinstance(value, str) and parent_id in value:
                                dependent_resources.append(resource)
                                break
                            elif isinstance(value, dict):
                                for k, v in value.items():
                                    if isinstance(v, str) and parent_id in v:
                                        dependent_resources.append(resource)
                                        break
        
        # Si encontramos recursos dependientes, crear un cluster anidado
        if dependent_resources:
            # Determinar un nombre apropiado para el cluster
            if parent_type == 'aws_ecs_cluster':
                cluster_name = f"ECS Cluster: {parent_name}"
            elif parent_type == 'aws_eks_cluster':
                cluster_name = f"EKS Cluster: {parent_name}"
            elif parent_type == 'aws_rds_cluster':
                cluster_name = f"RDS Cluster: {parent_name}"
            elif parent_type == 'aws_autoscaling_group':
                cluster_name = f"ASG: {parent_name}"
            elif parent_type == 'aws_lb' or parent_type == 'aws_alb' or parent_type == 'aws_elb':
                cluster_name = f"Load Balancer: {parent_name}"
            else:
                cluster_name = f"Dependencias de {parent_name}"
            
            # Crear un cluster para los recursos dependientes
            with Cluster(cluster_name):
                # Agrupar recursos dependientes por tipo para mejor organización
                dependent_by_type = {}
                for resource in dependent_resources:
                    resource_type = resource['type']
                    if resource_type not in dependent_by_type:
                        dependent_by_type[resource_type] = []
                    dependent_by_type[resource_type].append(resource)
                
                # Si hay múltiples tipos, crear subclusters por tipo
                if len(dependent_by_type) > 1:
                    for resource_type, type_resources in dependent_by_type.items():
                        friendly_name = resource_type.replace('aws_', '').replace('_', ' ').title()
                        
                        with Cluster(f"{friendly_name}"):
                            for resource in type_resources:
                                self._process_resource_node(resource)
                                # Llamada recursiva para crear clusters anidados más profundos
                                if resource['type'] in ['aws_ecs_cluster', 'aws_eks_cluster', 'aws_rds_cluster', 'aws_autoscaling_group', 'aws_lb', 'aws_alb', 'aws_elb']:
                                    self._create_nested_dependencies(resource, all_resources, depth + 1, max_depth, processed_resources)
                else:
                    # Si solo hay un tipo, no crear subcluster adicional
                    for resource in dependent_resources:
                        self._process_resource_node(resource)
                        # Llamada recursiva para crear clusters anidados más profundos
                        if resource['type'] in ['aws_ecs_cluster', 'aws_eks_cluster', 'aws_rds_cluster', 'aws_autoscaling_group', 'aws_lb', 'aws_alb', 'aws_elb']:
                            self._create_nested_dependencies(resource, all_resources, depth + 1, max_depth, processed_resources)
    
    def _process_resource_node(self, resource):
        """Processes a resource and creates its corresponding node"""
        address = resource['address']
        name = resource['name']
        resource_type = resource['type']
        
        # Evitar crear nodos duplicados
        if address not in self.nodes:
            # Caso especial para subnets
            if resource_type == 'aws_subnet':
                node_class = self._determine_subnet_type(resource)
            else:
                node_class = self.AWS_RESOURCE_MAP.get(resource_type, General)
            
            self.nodes[address] = node_class(f"{name}")