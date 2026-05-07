variable "service_account_key_file" {
  type = string
}

variable "cloud_id" {
  type = string
}

variable "folder_id" {
  type = string
}

variable "zone" {
  type    = string
  default = "ru-central1-a"
}

variable "registry_name" {
  type    = string
  default = "lab17-registry"
}
