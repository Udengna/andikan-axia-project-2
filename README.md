INTERNAL UTILITY SERVICE — PRODUCTION DEPLOYMENT

This project transforms a locally run Flask application into a secure, automated, production-grade system using containerization, CI/CD, and cloud infrastructure.

OVERVIEW

The application is a simple internal utility service built with Flask. It has been upgraded from a manual setup to a fully automated deployment pipeline with:

Docker containerization
CI/CD pipeline
Secure secret management
Automated deployment to AWS EC2
Reverse proxy with HTTPS
Zero-downtime deployment strategy

ARCHITECTURE

Flow:

Developer → GitHub → CI/CD Pipeline → Docker Hub → EC2 → Nginx → Users

Components used:

GitHub Actions for CI/CD automation
Docker for containerization
Docker Hub as image registry
AWS EC2 as compute infrastructure
Nginx as reverse proxy
AWS Secrets Manager for runtime secrets
Let’s Encrypt for HTTPS

DOCKERIZATION

Multi-stage build used for smaller image size
Non-root user improves security
.dockerignore excludes unnecessary files
HEALTHCHECK ensures container health monitoring

Run locally:

docker build -t internal-app .
docker run -p 5000:5000 internal-app

SECRETS MANAGEMENT

CI/CD secrets stored in GitHub Secrets
Runtime secrets stored in AWS Secrets Manager
EC2 accesses secrets via IAM Role (no credentials in code)

CI/CD PIPELINE

Pipeline stages:

Test
flake8 for linting
pytest for testing
Build
Docker multi-stage build
Push
Images pushed to Docker Hub
Deploy
Automatic deployment to EC2 via SSH
Blue-green deployment strategy

DOCKER TAGGING STRATEGY

latest → most recent build
v1.0.X → versioned releases
commit SHA → exact traceability

DEPLOYMENT STRATEGY (BLUE-GREEN)

Two containers run simultaneously:

internal-app-blue (port 5001)
internal-app-green (port 5002)

Deployment process:

Deploy new version to inactive environment
Run health check
Switch traffic via Nginx
Keep old version for rollback

This ensures zero downtime and fast recovery.

NGINX REVERSE PROXY

Routes traffic to active container
Handles HTTP to HTTPS redirection
Serves as the single entry point

HTTPS SETUP

SSL certificates generated using Let’s Encrypt
Configured using Certbot
Automatic renewal enabled

HEALTH CHECKS

Docker HEALTHCHECK monitors container status
/health endpoint validates application readiness
CI/CD waits for a healthy response before switching traffic

DEPLOYMENT (AWS EC2)

EC2 setup includes:

Docker installed
Nginx configured
IAM Role attached for Secrets Manager access
Security groups allowing only required ports (80 and 443)

FAILURE SIMULATIONS

The system supports:

Test failure blocking deployment
Container crash with auto-restart
Missing secret causing application failure
Rollback to previous version

SCALING STRATEGY

To scale the system:

Use a Load Balancer
Implement Auto Scaling Group
Run multiple EC2 instances

This enables horizontal scaling and high availability.

KNOWN LIMITATIONS

Single EC2 instance creates a single point of failure
Limited monitoring and logging
IAM permissions could be further restricted

FUTURE IMPROVEMENTS

Migrate to Kubernetes
Add monitoring tools (Prometheus, Grafana)
Implement Web Application Firewall (WAF)
Use Infrastructure as Code (Terraform)

REFLECTION SUMMARY

Multi-stage Docker builds improve efficiency and security
Blue-green deployment ensures zero downtime
Separating secrets improves security posture
CI/CD enables full automation and reproducibility

SUBMISSION EVIDENCE

Include screenshots of:

CI/CD pipeline success and failure
Docker Hub image tags
Running containers on EC2
HTTPS working with valid SSL certificate
Nginx configuration
Blue-green deployment switch

CONCLUSION

This project demonstrates the transition from a manual and insecure development setup to an automated, secure, and production-ready deployment system, focusing on automation, security, reliability, and scalability.
