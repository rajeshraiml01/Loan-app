resource "azurerm_kubernetes_cluster" "this" {
  name                = "${local.name_prefix}-aks"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  dns_prefix          = "${local.name_prefix}-dns"
  kubernetes_version  = var.kubernetes_version
  sku_tier            = "Standard"

  default_node_pool {
    name                 = "system"
    node_count           = var.node_count
    vm_size              = var.node_vm_size
    os_disk_type         = "Managed"
    auto_scaling_enabled = false
  }

  identity {
    type = "SystemAssigned"
  }

  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.this.id
  }

  network_profile {
    network_plugin    = "kubenet"
    load_balancer_sku = "standard"
    network_policy    = "calico"
  }

  oidc_issuer_enabled       = true
  workload_identity_enabled = true
  image_cleaner_enabled     = true
  image_cleaner_interval_hours = 48

  tags = local.common_tags
}

resource "azurerm_role_assignment" "acr_pull" {
  scope                = azurerm_container_registry.this.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.this.kubelet_identity[0].object_id
}
