# One-command start and stop for the course environment.
# Run `make help` to see every target.

CLUSTER      := owasp-gated-release
KIND_CONFIG  := infrastructure/kind/cluster.yaml

.DEFAULT_GOAL := help
.PHONY: help up down status

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-8s %s\n", $$1, $$2}'

up: ## Create the local cluster (does nothing if it already exists)
	@if kind get clusters | grep -qx "$(CLUSTER)"; then \
		echo "Cluster '$(CLUSTER)' already exists. Nothing to do."; \
	else \
		kind create cluster --config $(KIND_CONFIG); \
	fi
	@kubectl wait --for=condition=Ready nodes --all --timeout=120s --context kind-$(CLUSTER)

down: ## Delete the local cluster and everything in it
	kind delete cluster --name $(CLUSTER)

status: ## Show the cluster's nodes
	@kubectl get nodes -o wide --context kind-$(CLUSTER)
