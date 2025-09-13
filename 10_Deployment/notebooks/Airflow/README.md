# Apache Airflow  
https://airflow.apache.org/

## Amazon Managed Workflows for Apache Airflow (MWAA)  
https://ap-south-1.console.aws.amazon.com/mwaa/home?region=ap-south-1#home?landingPageCheck=1

- Deploy Airflow rapidly at scale
- Run Airflow with built-in security
- Reduce operational costs
- Use a pre-existing plugin or use your own.  
	Connect to any AWS or on-premise resources required for your workflows including Athena, Batch, Cloudwatch, DynamoDB, DataSync, EMR, ECS/Fargate, EKS, Firehose, Glue, Lambda, Redshift, SQS, SNS, Sagemaker, and S3.

Apache Airflow  
Apache Airflow is a platform created by the community to programmatically author, schedule and monitor workflows.


Directed Acyclic Graph (DAG): A directed graph with no directed cycles, where edges (arrows) move from one vertex to another without forming a closed loop. They are used in various fields, including: 
- Computer Science 	: To represent tasks with dependencies and ensure a logical execution order. 
- Data Science 		: In data modeling to build and organize complex data pipelines. 

A DAG is a model that encapsulates everything needed to execute a workflow. Some DAG attributes include the following:
- Schedule				: When the workflow should run.
- Tasks					: tasks are discrete units of work that are run on workers.
- Task Dependencies		: The order and conditions under which tasks execute.
- Callbacks				: Actions to take when the entire workflow completes.
- Additional Parameters	: And many other operational details.



Steps to Get Started with Airflow on local Machine
1. Install Apache Airflow
   - Use pip to install Airflow and its dependencies.
   - Example: `pip install apache-airflow`

