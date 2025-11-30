# MiniApp – Kubernetes Deployment (Frontend + Backend + MariaDB + Ingress + TLS)

Dies ist ein vollständiges Kubernetes-Praxisprojekt bestehend aus:

- MariaDB (persistent)
- Python Flask Backend (REST API auf `/users`)
- Nginx Frontend (HTML + JS)
- Ingress Routing für `/` und `/users`
- TLS-Zertifikaten via mkcert
- eigener Domain: `miniapp.local`
- vollständig funktionierendem Reverse-Proxy durch ingress-nginx

---

# Architektur (ASCII Diagramm)

                 ┌──────────────────────────────┐
                 │        Browser / Client       │
                 │  https://miniapp.local        │
                 └──────────────┬───────────────┘
                                │ 443 / TLS
                                ▼
                   ┌────────────────────────┐
                   │   ingress-nginx        │
                   │ (Ingress Controller)   │
                   └──────────┬────────────┘
            ┌──────────────────┴───────────────────┐
            │                                      │
            ▼                                      ▼
 ┌───────────────────────┐               ┌───────────────────────┐
 │     Frontend Service  │               │     Backend Service   │
 │     ClusterIP:80      │               │     ClusterIP:3000     │
 └───────────┬───────────┘               └──────────┬────────────┘
             │                                       │
             ▼                                       ▼
   ┌───────────────────┐                    ┌──────────────────────┐
   │ Frontend Pods     │                    │ Backend Pod          │
   │ Nginx: index.html │                    │ Flask: /users        │
   └───────────────────┘                    └──────────┬───────────┘
                                                       │
                                                       ▼
                                            ┌──────────────────────┐
                                            │      MariaDB          │
                                            │  PVC: db-pvc          │
                                            └──────────────────────┘

---


# Projektstruktur

```
├── Projekt
│   ├── backend
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── docker-compose.yml
│   ├── frontend
│   │   ├── Dockerfile
│   │   └── index.html
│   └── k8s
│       ├── backend
│       │   └── backend.yml
│       ├── configmap.yml
│       ├── db
│       │   └── db.yml
│       ├── frontend
│       │   └── frontend-nodeport.yml
│       ├── frontend-lb.yml
│       ├── ingress.yml
│       ├── miniapp.local-key.pem
│       ├── miniapp.local.pem
│       ├── namespace.yml
│       ├── secret.yml
│       └── volume.yml
└── README.md
 
```

## Namespace erstellen

```bash
kubectl apply -f k8s/namespace.yml
```

## ConfigMap + Secret

```
kubectl apply -f k8s/configmap.yml
kubectl apply -f k8s/secret.yml
```

## Persistent Volume für MariaDB

```
kubectl apply -f k8s/volume.yml
```

## MariaDB

```
kubectl apply -f k8s/db/db.yml
kubectl get pods -n miniapp
kubectl get svc -n miniapp
```

## backend deploy

```
docker build -t smalbackend:v1 backend/
docker tag smalbackend:v1 stephanrdev/smalbackend:v1
docker push stephanrdev/smalbackend:v1
kubectl apply -f k8s/backend/backend.yml
kubectl port-forward svc/backend -n miniapp 30300:3000
curl http://localhost:30300/users
```

## Frontend deploy

```
docker build -t smalfrontend:v2 frontend/
docker tag smalfrontend:v2 stephanrdev/smalfrontend:v2
docker push stephanrdev/smalfrontend:v2
kubectl apply -f k8s/frontend/frontend-nodeport.yml
curl http://localhost:30080
```

## LoadBalancer Service

```
kubectl apply -f k8s/frontend-lb.yml
kubectl get svc -n miniapp
```
## Ingress - controller + structure mit Helm 

### installation Helm ###

```
## Windows (winget geht, sonst auch choco oder scoop)
winget install Helm.Helm
## Mac
brew install helm
## Linux (apt)
sudo apt-get install curl gpg apt-transport-https --yes
curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
## Linux (dnf)
sudo dnf install helm
...

```
### add ingress-nginx-controller repo
```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```
### install ingress-nginx-controller

```
helm install nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace

kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
``` 
### ingess deploy 
```
kubectl apply -f k8s/ingress.yml

```
## Host Eintrag

```

**Linux** => 192.168.0.8 miniapp.local (ip von Ingress controller)
**Windows** => 127.0.0.1 miniapp.local
```

### test path

```
curl http://miniapp.local
```

## TLS mit mkcert erstellen

### install mkcert
```
**Linux** => sudo apt install mkcert
mkcert --install
```
**Windows** => [GitHub](https://github.com/FiloSottile/mkcert/releases/tag/v1.4.4)

### Zertifikat erzeugen
```
mkcert miniapp.local
```
### TLS secret erzeugen

```
kubectl create secret tls miniapp-tls \
  --cert=miniapp.local.pem \
  --key=miniapp.local-key.pem \
  -n miniapp
```
## Debugging

Wenn der namespace neugestartet werden muss, muss auch das TLS Zertifikat neu erstellt werden. 

### check Zertifikat (Linux)

```
openssl s_client -connect miniapp.local:443 -servername miniapp.local </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer

```
### check secret

```
 kubectl get secret miniapp-tls -n miniapp -o yaml | head
```
 
