# 1. Definimos el proveedor
provider "google" {
  credentials = file("credenciales.json") # Usamos las credenciales
  project     = "dataengineerp"
  region      = "us-central1"
}

# 2. Creamos un recurso nuevo: Un Bucket de Storage
resource "google_storage_bucket" "bucket_backup" {
  name          = "fintech-backup-seguro-danielmarcel" # Modificable
  location      = "US"
  force_destroy = true # Permite borrarlo aunque tenga archivos

  lifecycle_rule {
    condition {
      age = 30 # Borrar archivos viejos después de 30 días
    }
    action {
      type = "Delete"
    }
  }
}