#cloud-config (bash_history)
write_files:
- path: '/ubuntu/td-agent.conf'
  permissions: '0440'
  content: |2
    <source>
      @type tail
      @id bash_history_tail
      path /usr/local/src/logs/*/.cli.log
      pos_file /var/log/td-agent/bash_history.log.pos
      <parse>
        @type tsv
        keys begin,host,time,cwd,cmd,output,prompt
      </parse>
      tag bash_history
    </source>

    <match bash_history>
      @type s3
      aws_key_id ${aws_key_id}
      aws_sec_key ${aws_sec_key}
      s3_bucket edurange

      store_as json
      path "scenarios/${scenario_id}/bash_history/"
      s3_object_key_format "%%{path}%%{hostname}/%%{time_slice}_%%{index}.%%{file_extension}"
      time_slice_format "%Y-%m-%dT%H:%MZ"
      time_slice_wait 1m

      <format>
        @type json
      </format>

      buffer_chunk_limit 256m
    </match>
runcmd:
- set -eu
- mv /ubuntu/td-agent.conf /etc/td-agent/td-agent.conf
- chown td-agent:td-agent /etc/td-agent/td-agent.conf
- service td-agent restart
