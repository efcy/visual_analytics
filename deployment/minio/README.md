# VAT Minio
Minio is needed for Metaflow



We will use the community edition.
https://github.com/minio/minio/tree/master/helm/minio


# TODOs
- figure out where data is stored, whats the deal with the multiple pods?

--- 
after successfull install it should say
MinIO can be accessed via port 9000 on the following DNS name from within your cluster:
minio.demos.svc.cluster.local

To access MinIO from localhost, run the below commands:

  1. export POD_NAME=$(kubectl get pods --namespace demos -l "release=minio" -o jsonpath="{.items[0].metadata.name}")

  2. kubectl port-forward $POD_NAME 9000 --namespace demos

Read more about port forwarding here: http://kubernetes.io/docs/user-guide/kubectl/kubectl_port-forward/

You can now access MinIO server on http://localhost:9000. Follow the below steps to connect to MinIO server with mc client:

  1. Download the MinIO mc client - https://min.io/docs/minio/linux/reference/minio-mc.html#quickstart

  2. export MC_HOST_minio-local=http://$(kubectl get secret --namespace demos minio -o jsonpath="{.data.rootUser}" | base64 --decode):$(kubectl get secret --namespace demos minio -o jsonpath="{.data.rootPassword}" | base64 --decode)@localhost:9000

  3. mc ls minio-local