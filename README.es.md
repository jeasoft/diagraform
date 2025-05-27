
# DiagraForm

DiagraForm es una herramienta Python que genera diagramas visuales a partir de archivos de estado de Terraform, facilitando la comprensión y visualización de tu infraestructura como código.

## Características

- Genera diagramas de infraestructura a partir de archivos de estado de Terraform
- Agrupa recursos por VPC o por tipo de recurso
- Filtra tipos específicos de recursos para incluir
- Excluye tipos específicos de recursos del diagrama
- Crea clusters anidados para recursos relacionados
- Detección inteligente de tipos de subredes (públicas/privadas)

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/jeasoft/diagraform.git
cd diagraform

# Instalar en modo desarrollo
pip install -e .

```

## Requisitos
- Python 3.9+
- Graphviz (requerido para la biblioteca diagrams)
- Terraform (para generar archivos de estado)
## Uso
### Uso Básico
```
# Generar un diagrama básico
diagraform generate /ruta/al/terraform.tfstate
```
### Filtrado de Recursos
Puedes filtrar para incluir solo tipos específicos de recursos:

```
# Incluir solo VPCs y subredes
diagraform generate /ruta/al/terraform.tfstate 
--filter aws_vpc --filter aws_subnet
```
### Exclusión de Recursos
Puedes excluir tipos específicos de recursos de tu diagrama:

```
# Excluir roles y políticas IAM
diagraform generate /ruta/al/terraform.tfstate 
--exclude aws_iam_role --exclude aws_iam_policy

# Excluir logs de CloudWatch
diagraform generate /ruta/al/terraform.tfstate 
--exclude aws_cloudwatch_log_group
```
### Agrupación de Recursos
Puedes agrupar recursos por VPC o por tipo de recurso:

```
# Agrupar por VPC
diagraform generate /ruta/al/terraform.tfstate 
--group-by vpc

# Agrupar por tipo de recurso
diagraform generate /ruta/al/terraform.tfstate 
--group-by type
```
### Clusters Anidados
Crea clusters anidados para recursos relacionados (especialmente útil para clusters ECS, EKS y RDS):

```
# Crear clusters anidados agrupados por VPC
diagraform generate /ruta/al/terraform.tfstate 
--group-by vpc --nested

# Crear clusters anidados agrupados por tipo 
de recurso
diagraform generate /ruta/al/terraform.tfstate 
--group-by type --nested
```

### Combinación de Opciones
Puedes combinar múltiples opciones para diagramas más específicos:

```
# Agrupar por VPC, crear clusters anidados y 
excluir recursos IAM
diagraform generate /ruta/al/terraform.tfstate 
--group-by vpc --nested --exclude aws_iam_role 
--exclude aws_iam_policy

# Filtrar para incluir solo recursos 
específicos y excluir otros
diagraform generate /ruta/al/terraform.tfstate 
--filter aws_vpc --filter aws_subnet --filter 
aws_instance --exclude aws_cloudwatch_log_group
```
### Análisis de Archivos de Estado
Puedes analizar un archivo de estado sin generar un diagrama:

```
diagraform analyze /ruta/al/terraform.tfstate
```

## Opciones de Línea de Comandos

| Opción | Descripción |
|--------|-------------|
| `state_file` | Ruta al archivo de estado de Terraform (requerido) |
| `--output`, `-o` | Directorio de salida para el diagrama (predeterminado: ./diagrams) |
| `--filename`, `-f` | Nombre del archivo de salida sin extensión (predeterminado: terraform_diagram) |
| `--show/--no-show` | Abrir el diagrama después de la generación (predeterminado: --show) |
| `--filter`, `-t` | Filtrar para incluir solo tipos específicos de recursos (se puede usar múltiples veces) |
| `--exclude`, `-e` | Excluir tipos específicos de recursos (se puede usar múltiples veces) |
| `--group-by`, `-g` | Agrupar recursos por 'vpc', 'type', o 'none' (predeterminado: none) |
| `--nested/--no-nested` | Crear clusters anidados para recursos relacionados (predeterminado: --no-nested) |

## Ejemplos
### Diagrama Básico
```
diagraform generate /ruta/al/terraform.tfstate
```
### Excluyendo Recursos IAM
```
diagraform generate /ruta/al/terraform.tfstate 
--exclude aws_iam_role --exclude aws_iam_policy
```
### Agrupación Anidada por VPC
```
diagraform generate /ruta/al/terraform.tfstate 
--group-by vpc --nested
```

## Advertencia
**Usé una herramienta de AI para realizar este proyecto**
Por ahora solo funciona con recursos AWS.
Este proyecto está en desarrollo. Use con precaución.

## Licencia
MIT