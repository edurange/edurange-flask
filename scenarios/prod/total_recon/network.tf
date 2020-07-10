


/*

      NAT Gateway








*/

resource "aws_vpc" "total_recon" {
  cidr_block = "10.0.0.0/16"
  tags = merge(local.common_tags, { Name        = "total_recon" })
}

resource "aws_internet_gateway" "total_recon" {
  vpc_id = aws_vpc.total_recon.id
  tags = merge(local.common_tags, { Name = "total_recon" })
}

resource "aws_subnet" "home" {
  vpc_id     = aws_vpc.total_recon.id
  cidr_block = "10.0.129.0/24"
  tags = merge(local.common_tags, { Name = "total_recon/nat" })
}


resource "aws_eip" "nat" {
  vpc                       = true
  associate_with_private_ip = "10.0.129.5"
  depends_on                = [aws_internet_gateway.total_recon]
  tags = merge(local.common_tags, { Name = "total_recon/nat" })
}


resource "aws_nat_gateway" "nat" {
  allocation_id = "${aws_eip.nat.id}"
  subnet_id     = "${aws_subnet.home.id}"
  tags = merge(local.common_tags, { Name = "total_recon/nat" })
}

resource "aws_route_table" "to_internet" {
  vpc_id = aws_vpc.total_recon.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.total_recon.id
  }
}

resource "aws_route_table" "through_nat" {
  vpc_id = aws_vpc.total_recon.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }
  tags = merge(local.common_tags, { Name = "total_recon" })
}

resource "aws_route_table_association" "home" {
  subnet_id      = aws_subnet.home.id
  route_table_id = aws_route_table.to_internet.id
}

# resource "aws_subnet" "home" {
#   vpc_id     = aws_vpc.total_recon.id
#   cidr_block = "10.0.24.0/24"
#   tags = merge(local.common_tags, { Name = "total_recon/home" })
# }

# resource "aws_route_table_association" "home" {
#   subnet_id      = aws_subnet.home.id
#   route_table_id = aws_route_table.private.id
# }

resource "aws_security_group" "allow_all_internal" {
  vpc_id = aws_vpc.total_recon.id
  name   = "total_recon/allow_all_internal"
  egress {
    self        = true
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
  }

  ingress {
    self        = true
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
  }
  tags = merge(local.common_tags, {
    Name = "total_recon/allow_all_internal"
  })
}

resource "aws_security_group" "ssh_ingress_from_world" {
  vpc_id = aws_vpc.total_recon.id
  name   = "total_recon/ssh_ingress_from_world"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = merge(local.common_tags, {
    Name = "total_recon/ssh_ingress_from_world"
  })
}


resource "aws_security_group" "http_egress_to_world" {
  vpc_id = aws_vpc.total_recon.id
  name   = "total_recon/http_egress_to_world"

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
  }

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
  }

  tags = merge(local.common_tags, {
    Name = "total_recon/http_egress_to_world"
  })
}

resource "aws_subnet" "earth" {
  vpc_id     = aws_vpc.total_recon.id
  cidr_block = "10.0.0.0/24"
  tags = merge(local.common_tags, { Name = "total_recon/earth" })
}

resource "aws_route_table_association" "earth" {
  subnet_id      = aws_subnet.earth.id
  route_table_id = aws_route_table.through_nat.id
}

resource "aws_subnet" "mars" {
  vpc_id     = aws_vpc.total_recon.id
  cidr_block = "10.0.192.0/18"
  tags = merge(local.common_tags, { Name = "total_recon/mars" })
}

resource "aws_route_table_association" "mars" {
  subnet_id      = aws_subnet.mars.id
  route_table_id = aws_route_table.through_nat.id
}
