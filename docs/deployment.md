# Visual Analytics Tool Deployment
Our live system is deployed in a k8s cluster. Applications running inside the k8s cluster are managed by argocd. 

To install ArgoCD in the cluster in the first place we need to manually install it:

```bash
# setup metalb if on-premise
kubectl apply -f deployment/metallb/metallb-native.yaml
# adjust addresspool to ip adress range of your public facing k8s nodes
kubectl apply -f deployment/metallb/addresspool.yaml

# setup ingress nginx
kubectl apply -f deployment/ingress-controller/controller.yaml

# setup argocd
kubectl create ns argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl apply -f deployment/argocd/
```
https://argo-cd.readthedocs.io/en/stable/getting_started/
https://medium.com/@rojenshrestha100/argo-cd-out-of-sync-due-to-cilium-identity-f9d6188aa056#:~:text=Solution%3A,documentation%20of%20argocd%20as%20well.&text=After%20applying%2C%20the%20Cilium%20Identity,will%20be%20back%20to%20synced.

TODO: how to update argocd?

## Setup TLS
At this point TLS does not work yet. For this we need to setup external secrets and cert-manager. External secrets is optional we use if for accessing secrets that are used for cloudflare access for the cert-manager DNS challenge. In our case we get the secrets from a shared 1Password account. You can provide the secrets in many other ways including creating the k8s secrets manually.

### 1Password Connector
I followed the setup from https://external-secrets.io/v0.9.20/provider/1password-automation/
Values reference for 1password connect: https://github.com/1Password/connect-helm-charts/blob/main/charts/connect/values.yaml
Note: I did not install the operator.

## Adding a new application to k8s