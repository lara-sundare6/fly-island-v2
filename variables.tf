variable "project" {
  description = "The GCP project to use"
  type        = string
}

variable "region" {
  description = "The GCP region to create resources in"
  type        = string
  default     = "us-central1"
}
