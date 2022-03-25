import json
import os


def get_file_name(path):
    return os.path.splitext(os.path.basename(path))[0]


SCHEMA_DIR = 'Files/models/schemas'
FILES = [file for file in os.listdir(SCHEMA_DIR) if os.path.isfile(os.path.join(SCHEMA_DIR, file))]
SCHEMAS = {
    get_file_name(file_name): json.load(open(os.path.join(SCHEMA_DIR, file_name)))
    for file_name in FILES
}


def get_file_validation_schema(schema_name):
    return SCHEMAS.get(schema_name, {})
