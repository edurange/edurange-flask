resource "aws_vpc" "cloud" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name        = "ssh_inception/cloud"
    scenario_id = var.scenario_id
  }
}

resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.cloud.id
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.cloud.id
  cidr_block = "10.0.129.0/24"
  tags = {
    Name = "ssh_inception/public"
  }
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.cloud.id
  cidr_block = "10.0.0.0/27"
  tags = {
    Name = "ssh_inception/private"
  }
}

resource "aws_security_group" "public" {
  name   = "ssh_inception/public"
  vpc_id = aws_vpc.cloud.id

  ingress {
    from_port   = "80"
    to_port     = "80"
    protocol    = "tcp"
    cidr_blocks = [aws_subnet.private.cidr_block]
  }

  ingress {
    from_port   = "443"
    to_port     = "443"
    protocol    = "tcp"
    cidr_blocks = [aws_subnet.private.cidr_block]
  }

  ingress {
    from_port   = "22"
    to_port     = "22"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
  }
}

resource "aws_security_group" "private" {
  name   = "ssh_inception/private"
  vpc_id = aws_vpc.cloud.id
  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
  }
  egress {
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.cloud.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.default.id
  }
}

resource "aws_route_table_association" "nat_subnet_route_table_association" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Route all traffic outbound from PlayerSubnet to NAT Instance
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.cloud.id

  route {
    cidr_block  = "0.0.0.0/0"
    instance_id = aws_instance.nat.id
  }
}

resource "aws_route_table_association" "player_subnet_route_table_association" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

