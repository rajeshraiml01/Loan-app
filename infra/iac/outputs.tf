output "resource_group_name" {
  description = "Resource group name for deployed Azure resources."
  value       = azurerm_resource_group.this.name
}

output "location" {
  description = "Azure region used for deployment."
  value       = azurerm_resource_group.this.location
}

output "aks_cluster_name" {
  description = "AKS cluster name."
  value       = azurerm_kubernetes_cluster.this.name
}

output "acr_name" {
  description = "Azure Container Registry name."
  value       = azurerm_container_registry.this.name
}

output "acr_login_server" {
  description = "Azure Container Registry login server."
  value       = azurerm_container_registry.this.login_server
}
