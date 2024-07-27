https://argo-cd.readthedocs.io/en/stable/getting_started/

# This is the only thing that will get deployed manually
k create ns argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml


https://medium.com/@rojenshrestha100/argo-cd-out-of-sync-due-to-cilium-identity-f9d6188aa056#:~:text=Solution%3A,documentation%20of%20argocd%20as%20well.&text=After%20applying%2C%20the%20Cilium%20Identity,will%20be%20back%20to%20synced.