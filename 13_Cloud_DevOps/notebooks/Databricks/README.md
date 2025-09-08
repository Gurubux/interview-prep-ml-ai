# Databricks

## Learning Sources
* [Databricks Academy](https://customer-academy.databricks.com/learn/catalog)

## Table of Contents

* [Core Architecture & SQL](#core-architecture--sql)
* [Governance, Catalog & Sharing](#governance-catalog--sharing)
* [Compute, Pipelines & Orchestration](#compute-pipelines--orchestration)
* [Workbench & Collaboration](#workbench--collaboration)
* [AI, GenAI & Intelligence Features](#ai-genai--intelligence-features)
* [Marketplace & Ecosystem](#marketplace--ecosystem)
* [Principles & Frameworks](#principles--frameworks)
* [Workspace vs Account (What lives where?)](#workspace-vs-account-what-lives-where)
* [Suggested First Learning Path](#suggested-first-learning-path)

---

## Core Architecture & SQL

* **Data Lakehouse (Architecture)**
  Unified platform that combines data-lake flexibility with data-warehouse performance for **BI + AI** on one foundation.
* **Delta Lake (Storage Layer)**
  Open table format with **ACID transactions**, schema enforcement/evolution, time travel—reliable analytics at scale.
* **Databricks SQL (Warehouse & BI)**
  Serverless SQL endpoints, dashboards, and governance integration for classic reporting and interactive analytics.
* **Lakehouse Federation**
  Query external data (other warehouses/lakes) **without copying**, while keeping governance consistent across sources.

---

## Governance, Catalog & Sharing

* **Unity Catalog (UC)**
  **Unified governance layer** for data & AI assets (tables, files, ML models, dashboards). Centralizes permissions, lineage, audit.
* **Catalog Explorer (Workspace UI)**
  Browse catalogs/schemas/tables, discover assets, preview data—**the day-to-day window into Unity Catalog**.
* **Delta Sharing (Open Protocol)**
  **Open, cross-platform** data sharing **without duplication**—share live tables securely with any recipient.
* **AI-Generated Table/Column Comments**
  Auto-enriched metadata to improve **search & natural-language** experiences across the catalog.

> ℹ️ **Account-Level (not Workspace):**
>
> * **Metastore Management** (attach UC metastores to workspaces, region scoping)
> * **Account Principals** (users, groups, service principals at the account scope)

---

## Compute, Pipelines & Orchestration

* **Serverless Compute**
  No cluster tuning; **simplified UX, faster scaling, improved reliability**; pay only for what you use.
* **Lakeflow Jobs (Orchestration)**
  **Orchestrate all job types** with control flows, triggers, retries, alerts & monitoring—core pipeline scheduler.
* **Databricks Workflows**
  End-to-end orchestration of notebooks, SQL, DLT, ML jobs—**modern replacement for ad-hoc schedulers**.
* **Delta Live Tables (DLT)**
  **Declarative ETL** for batch + streaming with **managed infrastructure**, expectations (data quality), and lineage built-in.

---

## Workbench & Collaboration

* **Databricks Notebooks**
  Collaborative, reproducible dev surface with **multi-language** support (SQL, Python, Scala, R) and rich outputs.
* **Databricks Assistant (in-product copilot)**
  AI helper for coding, debugging, query writing, doc lookup—**speeds up everyday development**.

---

## AI, GenAI & Intelligence Features

* **MosaicML / MosaicAI (Databricks GenAI)**
  Foundation for **training, fine-tuning, serving** LLMs on your data—accelerates GenAI application delivery.
* **AI/BI (Genie Spaces)**
  Natural-language analytics for non-technical users—**chat with your governed data** to get charts, insights, summaries.
* **Platform Intelligence (“under the hood”)**
  AI used to **understand structure/usage/meaning** of data and boost productivity (e.g., smarter search, NL interfaces).

---

## Marketplace & Ecosystem

* **Databricks Marketplace**
  Open marketplace for **data, analytics & AI products**—discover, collaborate, and **monetize** assets (with UC governance).

---

## Principles & Frameworks

* **Well-Architected Lakehouse Framework**
  Adapts cloud well-architected pillars to the lakehouse: **operational excellence, security, reliability, performance, cost**.
* **Open Source & Open Standards**
  Commitment to openness (e.g., Delta Lake, Delta Sharing) to avoid lock-in and enable interop.
* **Multi-Cloud Availability**
  Runs **across major clouds** with consistent governance via Unity Catalog.

---

## Workspace vs Account (What lives where?)

* **Workspace (you build & run)**

  * Notebooks
  * **Catalog Explorer**
  * **Lakeflow Jobs / Workflows**
  * SQL Warehouses / Dashboards
  * DLT pipelines
* **Account (you govern & connect)**

  * **Unity Catalog Metastore Management**
  * **Account Principals** (users, groups, service principals)
  * Workspace provisioning & cross-workspace policies

> Quick rule: **Workspace = Build & Operate**. **Account = Govern & Connect**.

---

## Suggested First Learning Path

1. **Lakehouse & Delta Lake basics** → create a table, test **ACID** & **time travel**.
2. **Unity Catalog** → set up permissions, explore assets in **Catalog Explorer**.
3. **Databricks SQL** → run queries, build a dashboard, practice warehousing patterns.
4. **DLT** → build a **declarative** batch+stream pipeline with expectations (data quality).
5. **Workflows / Lakeflow Jobs** → productionize your pipeline with retries, alerts, triggers.
6. **Serverless** → migrate a job to serverless, note reliability & scaling improvements.
7. **Delta Sharing** → publish a live table to a consumer **without copying** data.
8. **AI/BI (Genie) & Assistant** → ask natural-language questions; generate queries/visuals.
9. **MosaicAI** → fine-tune or serve a small LLM on a governed dataset (optional stretch).
10. **Marketplace** → subscribe to a dataset and use it in your SQL/DLT pipeline.

---

## Dashboard snapshot
![Databricks Dashboard Example](https://github.com/Gurubux/interview-prep-ml-ai/blob/main/13_Cloud_DevOps/notebooks/Databricks/databricks_dashboard.png)

## Databricks Certifications
![Databricks Fundamentals Certificate](https://github.com/Gurubux/interview-prep-ml-ai/blob/main/Certificates/2308_3_1008963_1757288113_Databricks%20-%20Generic.pdf)
