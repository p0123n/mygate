#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import distutils.core

VERSION = "3.0"

distutils.core.setup(
    name="mygate",
    version=VERSION,
    py_modules=["mygate"],
    author="P0123N",
    author_email="p0123n@outlook.com",
    url="https://github.com/p0123n/mygate",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="Another one lightweight wrapper around MySQLdb.",
)
