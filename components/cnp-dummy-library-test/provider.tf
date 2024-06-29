terraform {
  backend "azurerm" {}
  required_version = "0.13.0"
  required_providers {
    azuread = {
      source  = "hashicorp/azuread"
      version = "2.53.1"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.41.0"
    }
    azuredevops = {
      source  = "microsoft/azuredevops"
      version = "0.1.0"
    }
    pkcs12 = {
      source  = "chilicat/pkcs12"
      version = "0.0.7"
    }
    panos = {
      source  = "PaloAltoNetworks/panos"
      version = "1.11.0"
    }
    github = {
      source  = "integrations/github"
      version = "5.3.0"
    }
    dynatrace = {
      version = "1.18.1"
      source  = "dynatrace-oss/dynatrace"
    }
  }
}
