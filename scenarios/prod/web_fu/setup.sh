#!/bin/bash
set -euxo pipefail

certConfig="/etc/apache2/sites-enabled/default-ssl.conf"
latestCert=$(ls -1  /etc/ssl/webfu/cert* | sed -e '$!d')

if [[ `grep $latestCert $certConfig` -eq 1 ]]; then
  echo "[i] No need to update SSL certificate.";
else
  latestKey=$(ls -1  /etc/ssl/webfu/privkey* | sed -e '$!d')
  sed -i "/\t\tSSLCertificateFile/c\\\t\tSSLCertificateFile\t$latestCert" $certConfig
  sed -i "/\t\tSSLCertificateKeyFile/c\\\t\tSSLCertificateKeyFile $latestKey" $certConfig
  echo "[i] SSL certificate and key updated!";
fi

service apache2 start
service mysql start
