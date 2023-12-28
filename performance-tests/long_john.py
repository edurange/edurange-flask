from tqdm import tqdm
import paramiko
import time


# Update the next four lines with your
# server's information

host = "34.68.235.15"
u = "dagroupuser1"
p = "8CRES8vcD6Ia7d2F"
edu_port = 32779


client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, port=edu_port, username=u, password=p, look_for_keys=False)
# time.sleep(.01)


# test
sftp = client.open_sftp()
try:
    sftp.mkdir('/tmp/test')
    print("Directory created successfully")
except IOError as e:
    print("Directory already exists, but it was just for a test")

print("Creating dummy file")
# Create a large dummy file of 1 GB in the /tmp/test directory
_, stdout, _ = client.exec_command('dd if=/dev/zero of=/tmp/test/large_file bs=1G count=1')
stdout.channel.recv_exit_status()

print("file created")

remote_file_size = sftp.stat('/tmp/test/large_file').st_size

# numbers on the progress bar are wrong

progress_bar = tqdm(total=remote_file_size, unit='B', unit_scale=True, desc="/tmp/test/large_file")

def mycallback(data, file_size):
    progress_bar.update(data)



# and now send that file over the network for stress testing
local_path = "/Users/cart/edurange/edurange-test/tlogs/large_file"  # use your own path here
sftp.get('/tmp/test/large_file', local_path, callback=mycallback)

progress_bar.close()


print("got the treasure!")

sftp.close()
client.close()

