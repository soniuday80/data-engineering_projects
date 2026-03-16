terraform {
  required_providers {
    snowflake = {
      source  = "snowflakedb/snowflake"
      version = "~> 0.98" # changed the version
    }
  }
}

provider "snowflake" {
  alias   = "terraform"
  organization_name = var.snowflake_org
  account_name      = var.snowflake_account
  user              = "TF_SERVICEUSER"
  role              = "SYSADMIN"
  authenticator     = "SNOWFLAKE_JWT"
  private_key       = file(var.snowflake_private_key_path)
}

resource "snowflake_database" "main" {
  provider = snowflake.terraform
  name     = "news_intelligence_db"
}

resource "snowflake_warehouse" "news_WH" {
  provider       = snowflake.terraform
  name           = "NEWS_INGESTION_WH"
  warehouse_size = "xsmall"
  auto_suspend   = 60
}

resource "snowflake_schema" "datawarehouse" {
  provider   = snowflake.terraform
  database   = snowflake_database.main.name
  name       = "data_schema"
}


