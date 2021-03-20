from __future__ import print_function
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
from kubernetes import client,config,watch
import os

configuration = kubernetes.client.Configuration()
# Configure API key authorization: BearerToken
configuration.api_key['authorization'] = os.getenv('KUBE_TOKEN')# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
configuration.api_key_prefix['authorization'] = 'Bearer'

# Defining host is optional and default to http://localhost
configuration.host = "https://1e4bb5fd-505e-4795-a4a8-bca4e2c7e55d.k8s.ondigitalocean.com"
configuration.user = "do-nyc3-snug-cluster-admin"
configuration.verify_ssl = False

# Enter a context with an instance of the API kubernetes.client
with kubernetes.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = kubernetes.client.CustomObjectsApi(api_client)
    group = 'hostkraken.com' # str | the custom resource's group
version = 'v1' # str | the custom resource's version
namespace = 'wordpress' # str | The custom resource's namespace
plural = 'restorejobs' # str | the custom resource's plural name. For TPRs this would be lowercase plural kind.
name = os.getenv('JOB_TO_DELETE') # str | the custom object's name
grace_period_seconds = 0 # int | The duration in seconds before the object should be deleted. Value must be non-negative integer. The value zero indicates delete immediately. If this value is nil, the default grace period for the specified type will be used. Defaults to a per object value if not specified. zero means delete immediately. (optional)
orphan_dependents = True # bool | Deprecated: please use the PropagationPolicy, this field will be deprecated in 1.7. Should the dependent objects be orphaned. If true/false, the \"orphan\" finalizer will be added to/removed from the object's finalizers list. Either this field or PropagationPolicy may be set, but not both. (optional)
propagation_policy = 'propagation_policy_example' # str | Whether and how garbage collection will be performed. Either this field or OrphanDependents may be set, but not both. The default policy is decided by the existing finalizer set in the metadata.finalizers and the resource-specific default policy. (optional)
dry_run = 'dry_run_example' # str | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed (optional)
body = kubernetes.client.V1DeleteOptions() # V1DeleteOptions |  (optional)

try:
    api_response = api_instance.delete_namespaced_custom_object(group, version, namespace, plural, name, grace_period_seconds=grace_period_seconds, orphan_dependents=orphan_dependents, propagation_policy=propagation_policy, dry_run=dry_run, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomObjectsApi->delete_namespaced_custom_object: %s\n" % e)
