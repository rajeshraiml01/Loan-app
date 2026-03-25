locals {
  normalized_prefix = lower(regexreplace(var.prefix, "[^a-z0-9]", ""))
  name_prefix       = substr(local.normalized_prefix, 0, 18)
  common_tags       = merge(var.tags, { application = "loan-app" })
}

resource "random_string" "suffix" {
  length  = 6
  upper   = false
  special = false
}

resource "azurerm_resource_group" "this" {
  name     = "${local.name_prefix}-rg"
  location = var.location
  tags     = local.common_tags
}
