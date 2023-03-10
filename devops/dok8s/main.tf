data "digitalocean_kubernetes_versions" "current" {
  version_prefix = var.cluster_version
}


resource "digitalocean_kubernetes_cluster" "primary" {
  name    = var.product
  region  = var.cluster_region
  version = data.digitalocean_kubernetes_versions.current.latest_version


  # Enable auto upgrades
  maintenance_policy {
    start_time = "03:00"
    day        = "sunday"
  }


  node_pool {
    name = var.node_name
    size = var.worker_size
    #node_count = var.worker_count
    min_nodes = var.asg_min
    max_nodes = var.asg_max
  }
}
