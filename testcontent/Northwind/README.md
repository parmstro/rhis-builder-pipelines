## Northwind Multi-Tier Application

- Requires Ansible 2.9 or newer
- Expects RHEL 9.x hosts
- Requires 4 VMs: database, cache, application, load balancer

### Why Northwind?

The Northwind database is deliberately simple and universally known. Every
developer and DBA has encountered it. This is the point. When demonstrating
automated content delivery, patching workflows, and multi-tier deployment
patterns, the application domain should create zero distraction. Nobody needs
to learn a new schema or understand unfamiliar business logic. The
infrastructure automation is the star — Northwind stays out of its way.

### Purpose

This section is designed for use as a demonstration tool for Automated Content
Management with Satellite and Ansible Automation Platform. Unlike the existing
single-host test applications (JBoss, LAMP, WordPress), Northwind demonstrates
a realistic multi-tier deployment that closely resembles what operations teams
manage in production — traditional VMs running a layered application stack.

The application models what customers actually run: a database tier, a caching
tier, an application tier, and a load balancer tier. Each tier runs on its own
VM. The deployment, testing, and patching workflows exercise real cross-tier
dependencies and integration seams.

### Architecture

```
                    +-----------+
                    |  HAProxy  |  :80 frontend, :8404 stats
                    |  (nw_lb)  |
                    +-----+-----+
                          |
                    +-----+-----+
                    |   Django  |  :8080 (Apache + mod_wsgi)
                    |  (nw_app) |
                    +--+-----+--+
                       |     |
              +--------+     +--------+
              |                       |
        +-----+------+        +------+------+
        | PostgreSQL  |        |    Redis    |
        |   (nw_db)   |        |  (nw_cache) |
        |    :5432    |        |    :6379    |
        +-------------+        +-------------+
```

| Tier | Role | Group | Packages |
|------|------|-------|----------|
| Database | postgresql | nw_dbservers | postgresql-server, python3-psycopg2 |
| Cache | redis | nw_cacheservers | redis |
| Application | django_app | nw_appservers | httpd, python3, mod_wsgi, Django (venv) |
| Load Balancer | haproxy | nw_lbservers | haproxy |

### Playbook Contract

Northwind follows the standard 4-playbook contract used across all test
applications, plus per-tier build playbooks for workflow-driven deployment.

| Playbook | Purpose |
|----------|---------|
| `main.yml` | Full sequential deployment (imports per-tier playbooks) |
| `deploymenttest.yml` | Smoke test — validates each tier and connection point |
| `qa_test.yml` | Qualification — data integrity and order lifecycle |
| `prod_test.yml` | Production validation — pre-patch gate and post-patch check |
| `undeploy.yml` | Reverse-order teardown |

**Per-tier build playbooks** (used by AAP workflow job templates):

| Playbook | Tier | Dependencies |
|----------|------|-------------|
| `build_postgresql.yml` | Database | None |
| `build_redis.yml` | Cache | None |
| `build_django.yml` | Application | Requires PostgreSQL + Redis |
| `build_haproxy.yml` | Load Balancer | Requires Django/Apache |

Each per-tier playbook is self-contained — it includes the common role and can
run independently. The workflow orchestrates the dependency order; the playbooks
don't need to know about each other.

### Workflow Topology

The Northwind content delivery pipeline (`SOE_ContentDeliveryPipeline_Northwind`)
is an independent workflow with its own job templates. The numbering convention
encodes the execution order — sort templates by name to read the flow.

```
NWDev1 PublishContent
  NWDev2 PromoteToDev
    NWDev3 DeployServers (4 VMs)
      NWDev4 SnapshotServers
        NWDev5.1 BuildDB -----+  (parallel)
        NWDev5.2 BuildCache --+
          NWDev5.3 BuildApp      (converges — all_parents_must_converge)
            NWDev5.4 BuildLB
              NWDev5.5 TestDeployment  (linear)
                NWDev6 PromoteToQA
                  NWDev7 DeleteSnapshots
                    NWDev8S DeleteServers / NWDev8F PowerOffServers
```

The QA pipeline (`NWQA1-6`) mirrors this structure, promoting Qualification
to Production instead of Development to Qualification.

Key differences from the existing JBoss/LAMP/WordPress pipeline:
- **Independent workflow** — Northwind does not share templates with other apps
- **Per-tier build nodes** — the workflow models real tier dependencies
- **Parallel where possible** — DB and Cache build concurrently
- **Convergence** — App tier waits for both DB and Cache to complete
- **Linear testing** — validates each integration seam in order

### Test Framework

Tests are data-driven. Test cases are defined in YAML files under `testdata/`,
and a generic test runner (`tasks/run_test_cases.yml`) executes them. This
separates test data from test logic and supports both positive and negative
test cases.

```
testdata/
  deployment/         # Smoke tests (deploymenttest.yml)
    health.yml        #   Health endpoint (DB + Cache connectivity)
    categories.yml    #   Seed data validation (8 categories)
    products.yml      #   Seed data validation (10+ products)
    customers.yml     #   CRUD + negative cases (missing fields, 404s)
  qa/                 # Qualification tests (qa_test.yml)
    data_integrity.yml    # Referential integrity validation
    order_lifecycle.yml   # Full order lifecycle with chained refs
  prod/               # Production validation (prod_test.yml)
    synthetic_transaction.yml  # Non-destructive write/read/delete cycle
```

Test cases support a `register_as` / `use_ref` pattern for chaining — a
customer created in one test case can be referenced by ID in subsequent cases.

### Inventory and Groups

Northwind uses separate AAP inventories (`SOE_northwind_pipeline_inventory`,
`SOE_northwind_qa_pipeline_inventory`) with namespaced group names to avoid
collisions with other applications.

```ini
[Northwind:children]
nw_dbservers
nw_cacheservers
nw_appservers
nw_lbservers

[nw_dbservers]
testnwdb2.example.ca

[nw_cacheservers]
testnwcache2.example.ca

[nw_appservers]
testnwapp2.example.ca

[nw_lbservers]
testnwlb2.example.ca
```

### Vault Variables

The following vault variables must be defined (see `vault_SAMPLES/`):

| Variable | Purpose |
|----------|---------|
| `northwind_db_password_vault` | PostgreSQL application user password |
| `northwind_django_secret_vault` | Django SECRET_KEY |
| `northwind_haproxy_stats_password_vault` | HAProxy stats endpoint password |

### Satellite Integration

All 4 Northwind tiers use the same hostgroup and activation key:
- **Hostgroup**: `hg_x86_64_rhel9_vm/{dev,qa}/soe9_{dev,qa}_northwind`
- **Activation Key**: `SOE9_{dev,qa}_EPEL` (shared with WordPress — same content profile)
- **Content View**: `SOE9_EPEL`

### How to Use

**Standalone** (local control node with inventory file):

    ansible-playbook -i inventory main.yml

**Workflow-driven** (AAP Controller):

Job templates and workflows are defined in `rhis-builder-inventory` under
`group_vars/platform_installer/`:
- `aap_templates_northwind_dev.yml` — Dev pipeline job templates
- `aap_templates_northwind_qa.yml` — QA pipeline job templates
- `aap_workflow_northwind_dev.yml` — Dev workflow definition
- `aap_workflow_northwind_qa.yml` — QA workflow definition

Templates are registered in `aap_templates_list.yml` and
`aap_workflow_templates_list.yml` for automatic inclusion.

### Extending

To add a new tier (e.g., a message queue):
1. Create a role under `roles/`
2. Create a `build_<tier>.yml` playbook
3. Add the tier to `main.yml` imports
4. Add a job template (`NWDev5.xBuild<Tier>`) in the templates file
5. Wire the workflow node with appropriate dependencies
6. Add test cases under `testdata/` to validate the new seam
