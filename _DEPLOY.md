1. Deploy to Azure

| **Category**             | **Name**                        | **Value**                                      |
|--------------------------|----------------------------------|------------------------------------------------|
| Web App                  | Publisher                        | Microsoft                                      |
|                          | SKU                              | Basic (B1)                                     |
|                          | Estimated Price                  | $9.59 USD/month                                |
| Details                  | Subscription                     | add95dae-484b-4544-ab56-34d373a7b80b           |
|                          | Resource Group                   | rg_greg                                        |
|                          | App Name                         | green-field                                    |
|                          | Secure Unique Hostname           | Enabled                                        |
|                          | Publish Method                   | Code                                           |
|                          | Runtime Stack                    | Python 3.13                                    |
| App Service Plan (New)   | Name                             | ASP-rggreg-9236                                |
|                          | Operating System                 | Linux                                          |
|                          | Region                           | UK South                                       |
|                          | SKU                              | Basic                                          |
|                          | Size                             | Small                                          |
|                          | ACU                              | 100 total ACU                                  |
|                          | Memory                           | 1.75 GB                                        |
| Monitor + Secure         | Application Insights             | Not enabled                                    |
| Deployment               | Basic Authentication             | Enabled                                        |
|                          | Continuous Deployment            | Enabled                                        |
|                          | GitHub Account                   | greg-solomon-uk                                |
|                          | Organization                     | greg-solomon-uk                                |
|                          | Repository                       | msdocs-python-fastapi-webapp-quickstart       |
|                          | Branch                           | main                                           |
| Database (New)           | Server Name                      | green-field-server                             |
|                          | Engine                           | PostgreSQL - Flexible Server                   |
|                          | Compute Tier & Size              | GeneralPurpose Standard_D2s_v3                 |
|                          | Database Name                    | green-field-database                           |
|                          | Region                           | UK South                                       |
|                          | Username                         | quulpcjhye                                     |
|                          | Password                         | ****************                               |
| Networking               | Virtual Network                  | vnet-doeigvof (10.0.0.0/16)                    |
|                          | Outbound Subnet                  | subnet-qutmnjup (10.0.1.0/24)                  |

2. **Set the startup command in the portal**
   
* Settings -> Configuration -> Startup Command
* gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app


3. **Apply Access Restrictions (IP Whitelisting)**
   
* Go to App Service > Networking > Access Restrictions.
* Add rules to allow only your IP or your organization's IP range.
* Once a rule is added, all other traffic is implicitly denied.

4. **Enable Authentication (Easy Auth)**

* Go to App Service > Authentication.
* Add an identity provider (e.g., Microsoft, GitHub, Google).
* Set Unauthenticated requests to:
  * Log in with... (to redirect to login), or
  * HTTP 401 (to block unauthenticated users).
