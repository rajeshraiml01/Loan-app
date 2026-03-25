locals {
  acr_name = substr("${local.normalized_prefix}${random_string.suffix.result}acr", 0, 50)
}

resource "azurerm_container_registry" "this" {
  name                          = local.acr_name
  resource_group_name           = azurerm_resource_group.this.name
  location                      = azurerm_resource_group.this.location
  sku                           = "Standard"
  admin_enabled                 = false
  public_network_access_enabled = true
  tags                          = local.common_tags
}
