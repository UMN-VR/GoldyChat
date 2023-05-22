import subprocess

# Get the current date and time from a trusted source, e.g. time.google.com
ntp_server = "time.google.com"
ntp_command = ["sudo", "ntpdate", "-u", ntp_server]

# Run the ntpdate command to update the system time
subprocess.call(ntp_command)
