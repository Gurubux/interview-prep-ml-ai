# Deployment

This folder contains resources and projects related to deployment of ML/AI applications.

## Content Index (A-Z)

### A
- **Airflow Dashboard**: Visual interface for monitoring and managing Apache Airflow workflows
  - Location: `notebooks/Airflow/media/Airflow_dashboard.gif`, `Airflow_dashboard.mp4`
- **Apache Airflow**: Workflow orchestration platform for scheduling and monitoring data pipelines
  - Documentation: `notebooks/Airflow/README.md`
  - Project: `notebooks/Airflow/airflow_project/`
- **Astro CLI**: Simplified command-line interface for managing Apache Airflow deployments
- **Astronaut ETL DAG**: Example DAG demonstrating dynamic task mapping
  - Location: `notebooks/Airflow/airflow_project/dags/exampledag.py`
- **AWS Managed Workflows for Apache Airflow (MWAA)**: Managed Airflow service on AWS
  - Console: https://ap-south-1.console.aws.amazon.com/mwaa/home

### B
- **Bash Operator**: Airflow operator for executing bash commands
  - Used in: `notebooks/Airflow/airflow_project/dags/airflow_main.py`

### C
- **Containers**: Docker container configuration for local Airflow development
  - Dockerfile: `notebooks/Airflow/airflow_project/Dockerfile`

### D
- **DAG (Directed Acyclic Graph)**: Workflow representation in Airflow
  - Examples: `notebooks/Airflow/airflow_project/dags/`
- **Dependencies**: Task dependency management in Airflow workflows
- **Docker**: Containerization platform used for local Airflow setup
- **Dynamic Task Mapping**: Feature allowing dynamic task creation based on runtime data

### E
- **ETL (Extract, Transform, Load)**: Data pipeline pattern
  - Example: `notebooks/Airflow/airflow_project/dags/sample_dag.py` (weather_etl)
- **Exampledag.py**: Astronaut ETL example demonstrating TaskFlow API and dynamic mapping

### F
- **Firewall/Network**: Connection settings for Airflow deployments

### G
- **Graph View**: Visual representation of DAG task dependencies in Airflow UI

### H
- **Hello World DAG**: Basic demonstration DAG
  - Location: `notebooks/Airflow/airflow_project/dags/airflow_main.py`
- **HTTP/API**: API connections for data extraction tasks

### I
- **Include Folder**: Directory for additional files in Airflow projects
  - Location: `notebooks/Airflow/airflow_project/include/`

### J
- **Job Scheduling**: Configuring when Airflow workflows should run

### K
- **Kubernetes**: Container orchestration (referenced for cloud deployments)

### L
- **Localhost Development**: Running Airflow locally for development and testing
- **Load Data Tasks**: Loading transformed data to target destinations

### M
- **Media Files**: Visual demonstrations and tutorials
  - Location: `notebooks/Airflow/media/`
- **Metadata Database**: PostgreSQL database for Airflow state management

### N
- **Notebooks**: Learning resources and examples
  - Location: `notebooks/`

### O
- **Open Notify API**: External API for astronaut data (used in example)
- **Operators**: Building blocks for Airflow tasks
  - Examples: BashOperator, PythonOperator

### P
- **Plugins**: Custom extensions for Airflow functionality
  - Location: `notebooks/Airflow/airflow_project/plugins/`
- **PostgreSQL**: Airflow metadata database
- **Projects**: Structured workspace organization
- **Python Operator**: Airflow operator for running Python functions

### Q
- **Quality Checks**: Data validation and quality assurance in pipelines

### R
- **README Files**: Documentation for different components
- **Requirements**: Python package dependencies
  - Location: `notebooks/Airflow/airflow_project/requirements.txt`
- **Retry Configuration**: Setting up task retries for fault tolerance

### S
- **Sample DAG**: Weather ETL example demonstrating Extract-Transform-Load pattern
  - Location: `notebooks/Airflow/airflow_project/dags/sample_dag.py`
- **Scheduler**: Airflow component responsible for triggering tasks
- **Settings Configuration**: Airflow configuration files
  - Location: `notebooks/Airflow/airflow_project/airflow_settings.yaml`
- **Start/Stop Commands**: Managing Airflow local development server
- **Streamlit**: Interactive web application framework
  - Location: `streamlit/` (placeholder)

### T
- **Task Dependencies**: Defining execution order in workflows
- **TaskFlow API**: Modern Pythonic API for defining Airflow tasks
- **Tests**: Unit and integration tests for DAGs
  - Location: `notebooks/Airflow/airflow_project/tests/`
- **Triggerer**: Airflow component for deferred task execution
- **Transform Tasks**: Data transformation operations in pipelines

### U
- **UI (User Interface)**: Web interface for Airflow monitoring
  - Access: http://localhost:8080 (local development)

### V
- **Variables**: Storing dynamic configuration in Airflow
- **Version Control**: Git repository management for DAG code

### W
- **Weather ETL**: Complete ETL pipeline example with extract, transform, and load tasks
- **Web Server**: Airflow component serving the UI and API
- **Windows Setup**: Local development setup instructions for Windows
- **Workflows**: Automated sequences of tasks

### X
- **XCom (Cross-Communication)**: Mechanism for sharing data between tasks
  - Used in: `notebooks/Airflow/airflow_project/dags/sample_dag.py`

### Y
- **YAML Configuration**: Configuration files for Airflow settings
  - Location: `notebooks/Airflow/airflow_project/airflow_settings.yaml`

### Z
- **Zero Downtime**: Strategies for deploying without service interruption

---

## Quick Start

### Getting Started with Airflow Locally

1. **Install Astro CLI** (Windows):
   ```powershell
   winget install -e --id Astronomer.Astro
   ```

2. **Initialize Project**:
   ```bash
   cd notebooks/Airflow/airflow_project
   astro dev init
   ```

3. **Start Airflow**:
   ```bash
   astro dev start
   ```

4. **Access UI**: http://localhost:8080 (username: `admin`, password: `admin`)

For detailed setup instructions and troubleshooting, see [`notebooks/Airflow/README.md`](notebooks/Airflow/README.md).

## Project Structure

```
10_Deployment/
├── notebooks/
│   └── Airflow/
│       ├── airflow_project/
│       │   ├── dags/           # DAG definitions
│       │   ├── include/         # Additional files
│       │   ├── plugins/         # Custom plugins
│       │   ├── tests/           # Test files
│       │   ├── Dockerfile       # Container configuration
│       │   └── requirements.txt # Python dependencies
│       └── media/               # Visual demonstrations
├── streamlit/                   # Streamlit applications (placeholder)
└── README.md                    # This file
```

