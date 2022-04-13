# Cloud buffer

This repository contains files for starting server for cloud buffer service.

## About project

Cloud buffer is a service for storing data and accessing it from different devices over different OS. There is no more
need to use messengers or cloud disks to send a file or text from your laptop to phone and back.

## Setting up

OS Dependencies:

* Python3 interpreter v3.8+
* Redis server
* SQLDataBase (sqlite3 for default)

After installing OS dependencies run `setup.sh` to install all python package dependencies using `pip` and create
necessary directories for files to be stored in.

## Running

```shell
redis-server --port 6379
# run-db if non default is used
python3 manage.py runserver 8000
```

## API

### Authentication and users

- `/account/login`

  `GET` - returns web page for logging in

  `POST` - try to log the user in using given credentials

- `/account/registet`

  `GET` - returns registration web page

  `POST` - try to register the user using given credentials

- `/account/profile`

  `GET` - returns web page with user profile

### Files

- `/file/load`

  `GET` - return web page for loading file

  `POST` - sends the file to server, returns web page with link to file and QR-code for other users to get it

- `/file/get`

  `GET` - downloads file with corresponding token

- '/file/buffer'

  `GET` - returns data storing in cloud buffer

  data in response content and file type in the `X-Data-Type` header

  `POST` - sends data to cloud buffer

  data should be in request content and type in the `X-Data-Type` header

## Files storage rules

For now there supports 2 types of data - text and files. The value of header should be `text` for text data and `file`
for files. Files must contain a filename in requests, otherwise, the error code will be returned.

File storage theoretically supports both types of data, but there only API for files exists. Buffer supports both types
of data.

There is a time limit for files to store in storage, so they expire after `2 hours`
(can be changed in `CloudBuffer/config.py::EXPIRE_TIME`)

Also, there is a limit on number of files per user that can be stored. Old files are deleted if more files uploads to
server. (`CloudBuffer/config.py::MAX_FILES`)

Files are stored in `user_files` directory, buffer data in `user_files/_buffer`.