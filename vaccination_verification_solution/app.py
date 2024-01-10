#!/usr/bin/env python3
import aws_cdk as cdk

from vaccination_verification_cdk_stack.vax_demo_query_stack import DemoQueries


app = cdk.App()

DemoQueries(app, "DemoQueries")

app.synth()
