# Handy cases for troubleshooting docker issues

## Error while fetching server API version: ('Connection aborted.', FileNotFoundError(2, 'No such file or directory'))

From experience this usually refers to a missing `docker` installation and te solutions is to install the software so it is available in the terminal. See [documentation](https://docs.docker.com/engine/install/).

## Error while fetching server API version: ('Connection aborted.', PermissionError(13, 'Permission denied'))

No permissions to run `docker`, so the solution is to make it available

```bash
sudo chmod 666 /var/run/docker.sock
```

## Error while fetching server API version: ('Connection aborted.', PermissionError(61, 'Connection refused'))

- Make sure you are running docker.
