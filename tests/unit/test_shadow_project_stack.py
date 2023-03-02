import aws_cdk as core
import aws_cdk.assertions as assertions

from shadow_project.shadow_project_stack import ShadowProjectStack

# example tests. To run these tests, uncomment this file along with the example
# resource in shadow_project/shadow_project_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ShadowProjectStack(app, "shadow-project")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
