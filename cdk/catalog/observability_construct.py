import aws_cdk.aws_sns as sns
from aws_cdk import CfnOutput, Duration, RemovalPolicy
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_iam as iam
from aws_cdk import aws_kms as kms
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_sqs as sqs
from cdk_monitoring_constructs import (
    AlarmFactoryDefaults,
    CustomMetricGroup,
    LatencyThreshold,
    MetricFactory,
    MetricStatistic,
    MonitoringFacade,
    SnsAlarmActionStrategy,
)
from constructs import Construct

from cdk.catalog import constants


class ObservabilityConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        db: dynamodb.TableV2,
        functions: list[_lambda.Function],
        visibility_queue: sqs.Queue,
        visibility_topic: sns.Topic,
    ) -> None:
        super().__init__(scope, id_)
        self.id_ = id_
        self.notification_topic = self._build_topic()
        self._build_high_level_dashboard(self.notification_topic)
        self._build_low_level_dashboard(db, functions, self.notification_topic, visibility_queue, visibility_topic)

    def _build_topic(self) -> sns.Topic:
        key = kms.Key(
            self,
            'ObserveKey',
            description='KMS Key for SNS Topic Encryption',
            enable_key_rotation=True,  # Enables automatic key rotation
            removal_policy=RemovalPolicy.DESTROY,
            pending_window=Duration.days(7),
        )
        topic = sns.Topic(
            self,
            f'{self.id_}alarms',
            display_name=f'{self.id_}alarms',
            master_key=key,
            enforce_ssl=True,
        )
        # Grant CloudWatch permissions to publish to the SNS topic
        topic.add_to_resource_policy(
            statement=iam.PolicyStatement(
                actions=['sns:Publish'],
                effect=iam.Effect.ALLOW,
                principals=[iam.ServicePrincipal('cloudwatch.amazonaws.com')],
                resources=[topic.topic_arn],
            )
        )
        CfnOutput(self, id=constants.MONITORING_TOPIC, value=topic.topic_name).override_logical_id(constants.MONITORING_TOPIC)
        return topic

    def _build_metric_list(self, metrics_factory: MetricFactory, names: list[str], labels: list[str], title: str) -> CustomMetricGroup:
        metrics_list = [
            metrics_factory.create_metric(
                metric_name=name,
                namespace=constants.METRICS_NAMESPACE,
                statistic=MetricStatistic.N,
                dimensions_map={constants.METRICS_DIMENSION_KEY: constants.METRICS_DIMENSION_VALUE},
                label=label,
            )
            for name, label in zip(names, labels, strict=False)
        ]
        return CustomMetricGroup(metrics=metrics_list, title=title)

    def _build_high_level_dashboard(self, notification_topic: sns.Topic):
        high_level_facade = MonitoringFacade(
            self,
            f'{self.id_}HighFacade',
            alarm_factory_defaults=AlarmFactoryDefaults(
                actions_enabled=True,
                alarm_name_prefix=self.id_,
                action=SnsAlarmActionStrategy(on_alarm_topic=notification_topic),
            ),
        )
        high_level_facade.add_large_header('Platform Engineering Service Catalog High Level Dashboard')
        metrics_factory = high_level_facade.create_metric_factory()
        success_group = self._build_metric_list(
            metrics_factory=metrics_factory,
            names=['CreatedProducts', 'DeletedProducts', 'UpdatedProducts'],
            labels=['created products', 'deleted products', 'updated products'],
            title='Successful Product Requests',
        )
        failure_group = self._build_metric_list(
            metrics_factory=metrics_factory,
            names=['FailedCreatedProducts', 'FailedDeletedProducts', 'FailedUpdatedProducts'],
            labels=['failed create products', 'failed delete products', 'failed update products'],
            title='Failed Product Requests',
        )
        high_level_facade.monitor_custom(metric_groups=[success_group, failure_group], human_readable_name='KPIs', alarm_friendly_name='KPIs')

    def _build_low_level_dashboard(
        self, db: dynamodb.TableV2, functions: list[_lambda.Function], notification_topic: sns.Topic, queue: sqs.Queue, visibility_topic: sns.Topic
    ):
        low_level_facade = MonitoringFacade(
            self,
            f'{self.id_}LowFacade',
            alarm_factory_defaults=AlarmFactoryDefaults(
                actions_enabled=True,
                alarm_name_prefix=self.id_,
                action=SnsAlarmActionStrategy(on_alarm_topic=notification_topic),
            ),
        )
        low_level_facade.add_large_header('Platform Engineering Service Catalog Low Level Dashboard')

        low_level_facade.monitor_sqs_queue(queue=queue, alarm_friendly_name='Visibility Queue')
        low_level_facade.monitor_sns_topic(topic=visibility_topic, alarm_friendly_name='Visibility Topic')

        for func in functions:
            low_level_facade.monitor_lambda_function(
                lambda_function=func,
                add_latency_p90_alarm={'p90': LatencyThreshold(max_latency=Duration.seconds(5))},
            )
            low_level_facade.monitor_log(
                log_group_name=func.log_group.log_group_name,
                human_readable_name='Error logs',
                pattern='ERROR',
                alarm_friendly_name='error logs',
            )

        low_level_facade.monitor_dynamo_table(table=db, billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST)
