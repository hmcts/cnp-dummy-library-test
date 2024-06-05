variable "product" {
  type        = string
  default     = null
  description = "product variable required by cnp terraform template. Not in use by terraform"
}
variable "builtFrom" {
  type        = string
  default     = null
  description = "builtFrom variable required by cnp terraform template. Not in use by terraform"
}
variable "env" {
  type        = string
  description = "Name of the environment to build in"
}
