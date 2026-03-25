variable "subscription_id" {
  description = "Azure subscription ID used for deployment."
  type        = string
}

variable "prefix" {
  description = "Short prefix used in Azure resource names."
  type        = string
  default     = "loanapp"
}

variable "location" {
  description = "Azure region for all resources."
  type        = string
  default     = "eastus"
}

variable "kubernetes_version" {
  description = "Optional AKS Kubernetes version. Leave null to use Azure default supported version."
  type        = string
  default     = null
}

variable "node_count" {
  description = "Initial AKS system node count."
  type        = number
  default     = 2
}

variable "node_vm_size" {
  description = "VM size for AKS system node pool."
  type        = string
  default     = "Standard_D2s_v5"
}

variable "tags" {
  description = "Common tags for Azure resources."
  type        = map(string)
  default = {
    workload    = "loan-app"
    environment = "prod"
    managedBy   = "terraform"
  }
}
