# Apache Airflow  
Apache Airflow  
Apache Airflow is a platform created by the community to programmatically author, schedule and monitor workflows.

https://airflow.apache.org/


Directed Acyclic Graph (DAG): A directed graph with no directed cycles, where edges (arrows) move from one vertex to another without forming a closed loop. They are used in various fields, including: 
- Computer Science 	: To represent tasks with dependencies and ensure a logical execution order. 
- Data Science 		: In data modeling to build and organize complex data pipelines. 

A DAG is a model that encapsulates everything needed to execute a workflow. Some DAG attributes include the following:
- Schedule				: When the workflow should run.
- Tasks					: tasks are discrete units of work that are run on workers.
- Task Dependencies		: The order and conditions under which tasks execute.
- Callbacks				: Actions to take when the entire workflow completes.
- Additional Parameters	: And many other operational details.

## Amazon Managed Workflows for Apache Airflow (MWAA)  
https://ap-south-1.console.aws.amazon.com/mwaa/home?region=ap-south-1#home?landingPageCheck=1

- Deploy Airflow rapidly at scale
- Run Airflow with built-in security
- Reduce operational costs
- Use a pre-existing plugin or use your own.  
	Connect to any AWS or on-premise resources required for your workflows including Athena, Batch, Cloudwatch, DynamoDB, DataSync, EMR, ECS/Fargate, EKS, Firehose, Glue, Lambda, Redshift, SQS, SNS, Sagemaker, and S3.




--- 
## A) Steps to Get Started with Airflow on local Machine
Here’s a clean, single-file **README.md** you can drop into your repo.

### 0) Prereqs (Windows)

* Windows 10/11
* **Astro CLI** (installs Podman automatically via `winget`)
* Optional: **WSL2** (if you prefer Linux tooling)

### 1) Install Astro CLI

```powershell
winget install -e --id Astronomer.Astro
astro version
```

If `astro` isn’t found, open a **new** terminal (PATH refresh) or restart PyCharm.

### 2) (Optional) Install Apache Airflow directly (Linux/WSL only)

If you want pure OSS Airflow without Astro, do it in **WSL**:

```bash
# Example (adjust versions as needed)
python3.11 -m venv .venv && source .venv/bin/activate
AIRFLOW_VERSION=2.9.3
PYTHON_VERSION=3.11
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

But for Windows convenience, Astro is simpler.

### 3) Init a new Astro project

From your project folder:

```bash
astro dev init
```

This creates:

```
.
├─ dags/
├─ include/
├─ plugins/
└─ tests/
```

### 4) Start Airflow (containers)

```bash
astro dev start
```

* Web UI: **[http://localhost:8080](http://localhost:8080)**
  (Default creds in local dev are typically `admin` / `admin`.)
* To watch logs attached in the same terminal, just keep it open.

### 5) Stop / Restart

```bash
# If logs are attached, press: Ctrl + C
astro dev stop        # stop containers (keeps state)
astro dev restart     # stop + start
astro dev kill        # stop & remove local state for this project
```

### 6) “View of dashboard”

Open **[http://localhost:8080](http://localhost:8080)** → You’ll see the **DAGs list**:

* Toggle **On/Off** (pause/unpause) per DAG
* **Graph** view for dependencies
* **Grid** view for runs
* **XCom**, logs, task details, etc.

---

## B) Three Sample DAGs I Tried

> **How to use:** Put these files into your project’s `dags/` folder. Start with `astro dev start`, then open the UI and unpause/trigger.

### 1) `airflow_main.py` — Bash + TaskFlow mini-demo

### 2) `sample_dag.py` — Simple ETL (extract → transform → load)

### 3) `exampledag.py` — Astronauts API + dynamic task mapping (Astronomer SDK)

> Note: This uses `airflow.sdk` (Astronomer’s Airflow SDK). It runs in an **Astro** project. If you’re using pure OSS Airflow, replace `from airflow.sdk import dag, task` with `from airflow.decorators import dag, task` and drop `Asset` if unavailable.

---

### Troubleshooting I Hit (and Fixes)

* **`astro` works in one shell but not another** → Old shell didn’t inherit updated PATH. Open a **new** terminal or restart PyCharm.
* **Running a DAG with `python file.py`** → Don’t. Put it under `dags/` and let Airflow load it.
* **Windows import crash (`os.register_at_fork`)** → That’s native Windows Python. Run in **Astro container** or **WSL2**.
* **Port 8080 busy** → Stop previous stacks: `astro dev stop` or `astro dev kill`, check `podman ps`.

---

### What I Learned So Far

* The **right way** to run locally on Windows is via **containers** (Astro + Podman)—super smooth for Day 1.
* The **UI** is your friend: pause/unpause, trigger, inspect logs/XComs quickly.
* **TaskFlow API** (`@task`) makes Python functions feel natural as tasks; **operators** (e.g., `BashOperator`, `PythonOperator`) are still core building blocks.
* Small ETL examples (API → transform → print/DF) are perfect to learn **templating** and **XCom** flows.
* Astronomer’s **Airflow SDK** adds niceties (e.g., `Asset`, richer decorators). For pure OSS Airflow, use `from airflow.decorators import dag, task`.

---

### Next Steps

* Add retries, SLAs, alerts.
* Use connections/secrets (Airflow Connections & Variables).
* Try a real extract → load to a DB (e.g., Postgres) and schedule backfills.
* Add tests (unit + DAG validation) and CI checks with `astro` test tools.

---

### Astro CLI – project lifecycle (run from your Astro project folder)

```bat
astro version                          # Show Astro CLI version
astro dev init                         # Create Astro project (dags/, plugins/, etc.)
astro dev start                        # Build + start Airflow containers
astro dev stop                         # Stop containers (keeps state/volumes)
astro dev restart                      # Stop + start again
astro dev kill                         # Stop containers AND remove local state for this project
astro dev ps                           # List running project containers
astro dev logs                         # Tail logs from all services (Ctrl+C to stop tailing)
astro dev bash                         # Shell into the scheduler container
astro dev bash --container webserver   # Shell into a specific container
astro dev run airflow dags list        # Run a one-off command in the scheduler (default)
astro dev run --container webserver airflow version   # Run in a chosen container
```

### Day-to-day Airflow CLI (run **inside** the container via `astro dev bash` or `astro dev run …`)

```bash
airflow version
airflow dags list
airflow dags show <DAG_ID> --save     # Render DAG graph to a file
airflow dags pause <DAG_ID>           # Pause a DAG
airflow dags unpause <DAG_ID>         # Unpause a DAG
airflow dags trigger <DAG_ID>         # Manually trigger a run

airflow tasks list <DAG_ID>
airflow tasks test <DAG_ID> <TASK_ID> 2025-09-13   # Dry-run a single task locally
airflow tasks clear <DAG_ID> --only-running -y     # Clear running tasks (careful!)

airflow db check
airflow db migrate                     # Apply DB migrations (if needed)
# (Avoid reset on real work)
# airflow db reset -y
```

### Stopping & cleaning up (quick reference)

```bat
# If your terminal is attached to logs:
Ctrl + C

# Then:
astro dev stop        # Graceful stop
astro dev kill        # Hard stop + remove state for this project
```

### Podman fallbacks (if you need to inspect/force-stop containers)

```bat
podman ps
podman logs -f <CONTAINER_ID>
podman stop <CONTAINER_ID>
podman rm -f <CONTAINER_ID>
podman volume ls
podman system prune -a    # ⚠️ Cleans unused images/containers/volumes
```

###Path & shell helpers (Windows)

```bat
where astro                   # Verify astro.exe on PATH
astro dev stop --project-dir "D:\study\interview-prep-ml-ai\10_Deployment\notebooks\Airflow"
```

Tip: Don’t run DAG files with `python your_dag.py`. Put them in `dags/`, start with `astro dev start`, then use the Airflow UI ([http://localhost:8080](http://localhost:8080)) or the Airflow CLI commands above.
