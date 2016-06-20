# -*- coding: utf-8 -*-
from . import main
from flask import current_app
import logging

logger = logging.getLogger(__name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    return current_app.send_static_file('index.html')
