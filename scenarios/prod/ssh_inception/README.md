# Terraform SSH Inception

[Terraform](https://en.wikipedia.org/wiki/Terraform_(software)) is software that provisions cloud infrastructure from a declarative configuration language.
This repository is a proof of concept for configuring the EDURange scenario SSH Inception using terraform.

## Prerequisites

You must install the `terraform` command line tool.

## Running

* [`terraform init`](https://www.terraform.io/docs/commands/init.html)
* [`terraform apply`](https://www.terraform.io/docs/commands/apply.html)
* [`terraform destroy`](https://www.terraform.io/docs/commands/destroy.html)

## Variables

The scenario can be parameterized with files in the [`variables.auto.tfvars.json`](variables.auto.tfvars.json) file. This contains a list of player logins, passwords, flags, etc.

Currently password hashes have to be provided as variables. We could hash the plaintext passwords using the [terraform `bcrypt` function](https://www.terraform.io/docs/configuration/functions/bcrypt.html). However, since a new random salt is generated each time it would incorrectly mark any resource that uses the password as tainted.

You can generate a hash of `PASSWORD` in a linux shell with
```
$ openssl passwd -6 PASSWORD
$6$4IqCqvR8tz2FaRFr$CTnNKB707D/otiy114t/VVXXIgXWqX.fLFB4IhF2dS2h/aU7bwpSZPOGQmplg/WQrK5/hc8zWBaEAsGWOkmLj0
```

The utility [`create_variables`](create_variables) will make a [`variables.auto.tfvars.json`](variables.auto.tfvars.json) file:
```
$ ./create_variables > variables.auto.tfvars.json
```

