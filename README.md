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

This project demonstrates the transition from a manual and insecure development setup to an automated, secure, and production-ready deployment system, focusing on automation, security, reliability, and scalability.

REFLECTION ANSWERS

Why did you structure the Dockerfile the way you did?

So basically, I wanted the Docker image to be small, secure, and easy to rebuild. I used a slim Python image to avoid unnecessary bloat. I installed dependencies first so Docker can cache that layer and speed things up. I also made sure the app runs as a non-root user for security. Then I used a .dockerignore to avoid copying junk files, and added a health check so we can tell if the app is actually running. The idea was just to keep things clean and production-ready.

Why multi-stage?

Multi-stage just helps keep things tidy. I used one stage to build everything, and another for running the app. That way, the final image doesn’t include build tools or anything extra. It makes the image smaller and more secure.

Why that tagging strategy?

I used three tags so it’s easier to manage deployments.
“latest” is just the newest version.
The version tag (like v1.0.X) helps track releases.
And the commit SHA ties the image to a specific piece of code.

So if something breaks, I can quickly roll back or figure out exactly what changed.

Why GitHub Secrets + AWS Secrets Manager?

I split secrets based on where they’re used. GitHub handles CI/CD stuff like Docker login and SSH keys. But things like database credentials are stored in AWS Secrets Manager and pulled at runtime. That way, sensitive data isn’t exposed in the pipeline or inside the code.

How does your deployment avoid downtime?

I used a blue-green setup. Basically, I run two versions of the app at the same time. One is live, and the other gets updated. Once the new one passes a health check, Nginx switches traffic to it. Since the old version is still running during the switch, users don’t notice anything. No downtime.

How would you scale to multiple EC2 instances?

If traffic grows, I’d put a load balancer in front and run multiple EC2 instances. Then use auto scaling so more instances spin up when needed. Each instance would run the same Docker image and pull configs from a shared place.

What security risks still exist?

There are still a few risks. Everything is on one EC2 instance, so if that goes down, the app is down. Containers also share the host system, which has some risk. IAM permissions could be tighter, and there’s no WAF or advanced monitoring yet. So it’s good, but not perfect.

How would you evolve this into Kubernetes?

If I move this to Kubernetes, I’d let it handle most of the heavy lifting. Deployments would replace my manual blue-green setup, and an Ingress controller would replace Nginx. Kubernetes would also handle scaling and self-healing automatically. It basically takes what I built and makes it more scalable and easier to manage.
