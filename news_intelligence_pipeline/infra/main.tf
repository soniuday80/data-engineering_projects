terraform {
  required_providers {
    snowflake = {
      source  = "snowflakedb/snowflake"
      version = "~> 1.0" 
    }
  }
}

provider "snowflake" {
    organization_name = var.snowflake_org
    account_name      = var.snowflake_account
    user              = "TF_SERVICEUSER"
    role              = "SYSADMIN"
    authenticator     = "SNOWFLAKE_JWT"
    private_key       = file(var.snowflake_private_key_path)
}

resource "snowflake_database" "news_db" {
    name = "news_intelligence_db"
}

resource "snowflake_Warehouse" "news-wh"{
    name           = "NEWS_INGESTION_WH"
  warehouse_size = "X-SMALL"
  auto_suspend   = 60
  auto_resume    = true
}
