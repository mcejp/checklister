#!/usr/bin/env python3

import os
import subprocess
import sys

import jinja2
import yaml

INPUT, OUTPUT = sys.argv[1:]

with open(INPUT) as f:
    model = yaml.safe_load(f)

template_name = model["_template"]

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("."),
    trim_blocks=True,
    lstrip_blocks=True,
)

template = env.get_template(f"{template_name}.html")

with open("_out.html", "wt") as f:
    f.write(template.render(**model))

# https://github.com/wkhtmltopdf/wkhtmltopdf/issues/2590#issuecomment-143568303
conversion_args = []
if "_page_size" in model: conversion_args += ["-s", model["_page_size"]]
if "_page_width" in model: conversion_args += ["--page-width", model["_page_width"]]
if "_page_height" in model: conversion_args += ["--page-height", model["_page_height"]]

if "_postprocess_cmd" in model:
    temp_pdf = "_out.pdf"
    subprocess.check_call(["wkhtmltopdf"] + conversion_args + ["page", "_out.html", temp_pdf])
    subprocess.check_call(model["_postprocess_cmd"], shell=True, env={
        **os.environ,
        "INPUT": temp_pdf,
        "OUTPUT": OUTPUT,
    })
else:
    subprocess.check_call(["wkhtmltopdf"] + conversion_args + ["page", "_out.html", OUTPUT])
