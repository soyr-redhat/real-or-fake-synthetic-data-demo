# Deployment Guide - Real or Fake

## Prerequisites

- OpenShift cluster access
- GitHub repository with this code
- LLM API credentials (e.g., MAAS, OpenAI)

## Initial Setup

### 1. Create Namespace

```bash
oc new-project real-or-fake
```

### 2. Create Secrets

```bash
# Create secrets from example
cp deployment/secrets.yaml.example deployment/secrets.yaml

# Edit with your actual values
vim deployment/secrets.yaml

# Apply secrets
oc apply -f deployment/secrets.yaml
```

Required secrets:
- `llm-api-key`: Your LLM API authentication key
- `github-webhook-secret`: Secret for GitHub webhook authentication

### 3. Configure Backend URL

Edit `deployment/buildconfig.yaml` and update the frontend build arg:

```yaml
buildArgs:
- name: VITE_API_URL
  value: https://realorfake-backend-real-or-fake.apps.YOUR-CLUSTER-DOMAIN
```

### 4. Update Git Repository URL

In `deployment/buildconfig.yaml`, update the Git URI:

```yaml
git:
  uri: https://github.com/YOUR-ORG/YOUR-REPO.git
```

### 5. Deploy with Kustomize

```bash
oc apply -k deployment/
```

This will create:
- ConfigMap with LLM configuration
- PersistentVolumeClaim for leaderboard storage
- BuildConfigs and ImageStreams
- Deployments for backend and frontend
- Services and Routes

### 6. Trigger Initial Builds

```bash
# Start backend build
oc start-build realorfake-backend

# Start frontend build
oc start-build realorfake-frontend

# Watch build progress
oc logs -f bc/realorfake-backend
oc logs -f bc/realorfake-frontend
```

### 7. Verify Deployment

```bash
# Check pod status
oc get pods

# Check routes
oc get routes

# Get application URL
echo "https://$(oc get route real-or-fake -o jsonpath='{.spec.host}')"
```

## Automated CI/CD with GitHub Actions

### Setup GitHub Secrets

In your GitHub repository settings, add these secrets:

- `OPENSHIFT_LOGIN_TOKEN`: Your OpenShift login token
- `LLM_API_KEY`: LLM API key

### Get OpenShift Token

```bash
oc whoami -t
```

### Webhook Configuration

1. Get webhook URL from BuildConfig:
```bash
oc describe bc/realorfake-backend | grep "Webhook GitHub"
```

2. In GitHub repository settings:
   - Go to Settings → Webhooks → Add webhook
   - Paste the webhook URL
   - Content type: `application/json`
   - Secret: Use the same value as `github-webhook-secret` in secrets
   - Select "Just the push event"
   - Click "Add webhook"

3. Repeat for frontend BuildConfig

### Automated Workflow

When you push to the `main` branch with changes in:
- `2_synthetic_data/backend/**`
- `2_synthetic_data/frontend/**`
- `2_synthetic_data/deployment/**`

The GitHub Actions workflow will:
1. Login to OpenShift
2. Apply secrets and configs
3. Trigger new builds
4. Wait for build completion
5. Apply deployment manifests
6. Trigger pod rollouts
7. Clean up old builds

## Configuration Updates

### Update LLM Settings

```bash
# Edit configmap
oc edit configmap real-or-fake-config

# Or apply updated file
oc apply -f deployment/configmap.yaml
```

### Update Secrets

```bash
# Edit secrets
oc edit secret real-or-fake-secrets

# Restart pods to pick up changes
oc rollout restart deployment/realorfake-backend
```

### Scale Deployments

```bash
# Scale frontend
oc scale deployment/realorfake-frontend --replicas=3

# Scale backend
oc scale deployment/realorfake-backend --replicas=2
```

## Monitoring

### View Logs

```bash
# Backend logs
oc logs -f deployment/realorfake-backend

# Frontend logs
oc logs -f deployment/realorfake-frontend

# Build logs
oc logs -f bc/realorfake-backend
oc logs -f bc/realorfake-frontend
```

### Check Health

```bash
# Backend health
curl https://$(oc get route realorfake-backend -o jsonpath='{.spec.host}')/health

# Frontend (should return HTML)
curl https://$(oc get route real-or-fake -o jsonpath='{.spec.host}')
```

### View Leaderboard Data

```bash
# Get backend pod
BACKEND_POD=$(oc get pod -l app=realorfake-backend -o jsonpath='{.items[0].metadata.name}')

# View leaderboard file
oc exec $BACKEND_POD -- cat /data/leaderboard.json
```

## Troubleshooting

### Builds Failing

```bash
# Check build logs
oc logs -f bc/realorfake-backend

# Describe build for errors
oc describe build realorfake-backend-1
```

### Pods Not Starting

```bash
# Describe pod for events
oc describe pod -l app=realorfake-backend

# Check for image pull errors
oc get events --sort-by='.lastTimestamp'
```

### Backend Can't Connect to LLM

```bash
# Verify secrets
oc get secret real-or-fake-secrets -o yaml

# Check env vars in pod
oc exec deployment/realorfake-backend -- env | grep LLM
```

### Frontend Can't Reach Backend

1. Check backend route is accessible:
```bash
oc get route realorfake-backend
```

2. Verify VITE_API_URL in frontend build:
```bash
oc describe bc/realorfake-frontend | grep VITE_API_URL
```

3. Rebuild frontend if URL changed:
```bash
oc start-build realorfake-frontend
```

## Cleanup

```bash
# Delete all resources
oc delete all,pvc,configmap,secret -l app=real-or-fake

# Or delete entire project
oc delete project real-or-fake
```

## Production Considerations

1. **Persistent Storage**: The PVC uses default storage class. For production, specify storage class and increase size.

2. **Resource Limits**: Adjust CPU/memory limits in `deployment/deployment.yaml` based on load.

3. **High Availability**: Increase frontend replicas for better availability.

4. **Monitoring**: Set up Prometheus metrics and Grafana dashboards.

5. **Backup**: Regularly backup leaderboard PVC data.

6. **Rate Limiting**: Add rate limiting to prevent API abuse.

7. **CORS**: Restrict CORS origins in production backend.
