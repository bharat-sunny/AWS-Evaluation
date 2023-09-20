from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    aws_apigateway as api_gw,
    aws_sns as sns,
    aws_iam as iam,
    SecretValue,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild
    
)
from constructs import Construct

class InterviewProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        



























        # Create SNS Topic 
        topic = sns.Topic(self, "MyTopic", 
                      display_name="My SNS Topic",
                      topic_name="MyTopicName")


        # DynamoDB Tables
        users_table = ddb.Table(self, "UsersTable", table_name="UsersTable",
                                partition_key=ddb.Attribute(name="user_id", type=ddb.AttributeType.STRING))


        # orderTableName = OrdersTable
        orders_table = ddb.Table(self, "OrdersTable",  table_name="OrdersTable",
                                 partition_key=ddb.Attribute(name="order_id", type=ddb.AttributeType.STRING))

        # Lambda functions
        users_lambda = _lambda.Function(self, "UsersService",
                                        runtime=_lambda.Runtime.PYTHON_3_8,
                                        function_name="userService",
                                        handler="users.handler",
                                        code=_lambda.Code.from_asset("lambdas/users"),
                                        )

        notifications_lambda = _lambda.Function(self, "NotificationsService",
                                        runtime=_lambda.Runtime.PYTHON_3_8,
                                        function_name="notificationService",
                                        handler="notifications.handler",
                                        code=_lambda.Code.from_asset("lambdas/notifications"))
                                        
        orders_lambda = _lambda.Function(self, "OrdersService",
                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                         function_name="orderService",
                                         handler="orders.handler",
                                         code=_lambda.Code.from_asset("lambdas/orders"),
                                         environment={ "TARGET_LAMBDA_ARN": notifications_lambda.function_arn })

        # "NOTIFICATION_ENDPOINT": f"https://{self.node.try_get_context('stage')}.execute-api.{self.region}.amazonaws.com/prod/notifications_lambda"})


        notifications_lambda.add_permission("AllowInvoker", principal=notifications_lambda.role)

        
        # # Grant Lambda the permissions to send emails via SES
        notifications_lambda.add_permission("AllowOrderServiceInvoke", 
                                           action="lambda:InvokeFunction", 
                                           principal=orders_lambda.role)


        notifications_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"]
            )
        )

        users_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:VerifyEmailIdentity"],
                resources=["*"]
            )
        )
 

        # Granting permissions to Lambda to read/write from/to DynamoDB
        users_table.grant_read_write_data(users_lambda)
        orders_table.grant_read_write_data(orders_lambda)
        

        # API Gateway
        api = api_gw.RestApi(self, "MicroservicesApi",
                             rest_api_name="Microservices Service",
                             description="Gateway for Microservices.")
                    

        users_resource = api.root.add_resource('users')
        orders_resource = api.root.add_resource('orders')
        notification_resource = api.root.add_resource('notifications')


        notification_resource.add_method('GET', api_gw.LambdaIntegration(notifications_lambda))
        notification_resource.add_method('POST', api_gw.LambdaIntegration(notifications_lambda))

        users_resource.add_method('GET', api_gw.LambdaIntegration(users_lambda))
        users_resource.add_method('POST', api_gw.LambdaIntegration(users_lambda))

        orders_resource.add_method('GET', api_gw.LambdaIntegration(orders_lambda))
        orders_resource.add_method('POST', api_gw.LambdaIntegration(orders_lambda))

        
        
        
        
        # Create a CodePipeline
        pipeline = codepipeline.Pipeline(self, 'myMicroServices',
            pipeline_name='myMicroServices'
        )

        # Dev Stage
        source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.GitHubSourceAction(
            action_name='GitHub_Source',
            owner='bharat-sunny',
            repo='microservice',
            branch='main',  # Change to your desired branch
            oauth_token=SecretValue.secrets_manager('AWS'),  # Store your GitHub token in AWS Secrets Manager
            output=source_output
        )

        dev_stage = pipeline.add_stage(
            stage_name='Dev',
            actions=[source_action]
        )

        # To be uncommented when additional stages are needed

        # Test Stage
        test_build_project = codebuild.PipelineProject(
            self, 'TestBuildProject',
            build_spec=codebuild.BuildSpec.from_source_filename('buildspec-test.yml'),  # Create a buildspec file for your test stage
            environment=codebuild.BuildEnvironment(build_image=codebuild.LinuxBuildImage.STANDARD_4_0),
        )

        test_action = codepipeline_actions.CodeBuildAction(
            action_name='Test_Build',
            input=source_output,
            project=test_build_project
        )

        test_stage = pipeline.add_stage(
            stage_name='Test',
            actions=[test_action]
        )
#
#         # Deploy Stage
#         deploy_build_project = codebuild.PipelineProject(
#             self, 'DeployBuildProject',
#             build_spec=codebuild.BuildSpec.from_source_filename('buildspec-deploy.yml'),  # Create a buildspec file for your deploy stage
#             environment=codebuild.BuildEnvironment(build_image=codebuild.LinuxBuildImage.STANDARD_4_0),
#         )
#
#         deploy_action = codepipeline_actions.CodeBuildAction(
#             action_name='Deploy_Build',
#             input=source_output,
#             project=deploy_build_project
#         )
#
#         deploy_stage = pipeline.add_stage(
#             stage_name='Deploy',
#             actions=[deploy_action]
#         )

        # Connect the stages
        # deploy_stage.add_dependency(test_stage)
        # test_stage.add_dependency(dev_stage)
