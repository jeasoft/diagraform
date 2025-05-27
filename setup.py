from setuptools import setup, find_packages

setup(
    name="diagraform",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "diagrams>=0.23.3",
        "click>=8.1.3",
    ],
    entry_points={
        'console_scripts': [
            'diagraform=diagraform.cli:main',
        ],
    },
    author="Tu Nombre",
    author_email="tu@email.com",
    description="Generador de diagramas a partir de archivos de estado de Terraform",
    keywords="terraform, diagrams, aws, infrastructure",
    url="https://github.com/tuusuario/diagraform",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)