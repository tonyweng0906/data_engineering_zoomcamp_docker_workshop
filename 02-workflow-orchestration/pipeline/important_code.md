docker network create pg-network

docker-compose up -d

docker-compose down

**Kestra**
username: "admin@kestra.io" 
password: Admin1234!

PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=root

**When create pgadmin service**
Host_name = pgdatabase
POSTGRES_USER: root
POSTGRES_PASSWORD: root

# Add Service Account as a Secret

We can add our `Service Account` with the serviceAccount property to any of our Google Cloud or Workspaces tasks. To do this, we’ll need to add it as a secret to Kestra. There’s a number of ways to add secrets, but we’re going to add it via environment variables which will link to our Docker Compose file. If you want more information regarding how secrets work, check out the secrets page.

Once you have the service account file downloaded, you can rename it to `service-account.json`. Then we’ll encode the service account JSON and store it inside a file named `.env_encoded` which will hold all of our encoded secrets:

```bash
echo SECRET_GCP_SERVICE_ACCOUNT=$(cat service-account.json | base64 -w 0) >> .env_encoded
```

You can then set the `.env_encoded` file in your `docker-compose.yml`:

```bash
kestra:
  env_file: .env_encoded
```