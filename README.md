#Projektstruktur#

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
