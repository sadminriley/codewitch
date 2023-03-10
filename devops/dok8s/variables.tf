variable "product" {
  type    = string
  default = "aphrodite"
}

variable "cluster_version" {
  type    = string
  default = "1.25.4"
}

variable "worker_count" {
  type    = number
  default = 3
}

variable "worker_size" {
  type    = string
  default = "s-2vcpu-2gb"
}

variable "cluster_name" {
  type = string
}

variable "cluster_region" {
  type    = string
  default = "sfo3"
}

variable "node_name" {
  type    = string
  default = "default"
}

variable "asg_min" {
  type    = number
  default = 1
}

variable "asg_max" {
  type    = number
  default = 3
}
